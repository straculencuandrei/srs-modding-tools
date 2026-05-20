# Chunked binary search for strings in the large archive.ar
# Search for "InitialCash" byte pattern in chunks

$archivePath = "..\Data\archive.ar"
$searchTerms = @("InitialCash", "InitialRespect", "StartingGirl", "MP2GAMEDATA")
$chunkSize = 50MB
$overlapSize = 1024  # overlap to catch strings at chunk boundaries

$fileStream = [System.IO.File]::OpenRead($archivePath)
$fileLength = $fileStream.Length
Write-Host "Archive size: $fileLength bytes"

foreach ($term in $searchTerms) {
    Write-Host "`n=== Searching for: $term ==="
    $termBytes = [System.Text.Encoding]::ASCII.GetBytes($term)
    $fileStream.Position = 0
    $chunkIndex = 0
    $found = $false
    
    while ($fileStream.Position -lt $fileLength) {
        $pos = $fileStream.Position
        $readSize = [Math]::Min($chunkSize + $overlapSize, $fileLength - $pos)
        $buffer = New-Object byte[] $readSize
        $bytesRead = $fileStream.Read($buffer, 0, $readSize)
        
        # Search for the term in this chunk
        for ($i = 0; $i -lt ($bytesRead - $termBytes.Length); $i++) {
            $match = $true
            for ($j = 0; $j -lt $termBytes.Length; $j++) {
                if ($buffer[$i + $j] -ne $termBytes[$j]) {
                    $match = $false
                    break
                }
            }
            if ($match) {
                $absoluteOffset = $pos + $i
                Write-Host "  FOUND at offset: $absoluteOffset (hex: 0x$($absoluteOffset.ToString('X8')))"
                $found = $true
                
                # Hex dump context (200 bytes before, 300 bytes after)
                $dumpStart = [Math]::Max(0, $i - 200)
                $dumpEnd = [Math]::Min($bytesRead - 1, $i + 300)
                
                # ASCII context
                $contextBytes = $buffer[$dumpStart..$dumpEnd]
                $ascii = [System.Text.Encoding]::ASCII.GetString($contextBytes) -replace '[^\x20-\x7E]', '.'
                Write-Host "  ASCII context:"
                Write-Host "  $ascii"
                
                # Detailed hex dump (80 bytes around the match)
                Write-Host "`n  HEX DUMP:"
                $hexStart = [Math]::Max(0, $i - 32)
                $hexEnd = [Math]::Min($bytesRead - 1, $i + 80)
                for ($h = $hexStart; $h -lt $hexEnd; $h += 16) {
                    $hexLine = ""
                    $ascLine = ""
                    for ($k = 0; $k -lt 16; $k++) {
                        if (($h + $k) -lt $bytesRead) {
                            $hexLine += $buffer[$h + $k].ToString("X2") + " "
                            if ($buffer[$h + $k] -ge 0x20 -and $buffer[$h + $k] -le 0x7E) {
                                $ascLine += [char]$buffer[$h + $k]
                            } else {
                                $ascLine += "."
                            }
                        }
                    }
                    $absAddr = $pos + $h
                    Write-Host ("  0x{0:X8}: {1,-48} {2}" -f $absAddr, $hexLine, $ascLine)
                }
                Write-Host ""
                
                # Only show first 3 matches per term
                $matchCount++
                if ($matchCount -ge 3) { break }
            }
        }
        
        if ($found -and $matchCount -ge 3) { break }
        
        # Move to next chunk (with overlap)
        $fileStream.Position = $pos + $chunkSize
        $chunkIndex++
    }
    
    if (-not $found) {
        Write-Host "  NOT FOUND in archive"
    }
    $matchCount = 0
}

$fileStream.Close()
