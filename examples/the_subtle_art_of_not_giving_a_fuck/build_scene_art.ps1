# Automated StickLit 1080x1920 Scene Illustrator
param (
    [string]$scenesJson = "examples/the_subtle_art_of_not_giving_a_fuck/scenes.json",
    [string]$outputDir = "examples/the_subtle_art_of_not_giving_a_fuck/images"
)

Add-Type -AssemblyName System.Drawing

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$scenes = Get-Content -Path $scenesJson -Raw -Encoding UTF8 | ConvertFrom-Json

$fontHeadline = New-Object System.Drawing.Font("Arial", 46, [System.Drawing.FontStyle]::Bold)
$fontSub = New-Object System.Drawing.Font("Arial", 22, [System.Drawing.FontStyle]::Bold)
$fontTag = New-Object System.Drawing.Font("Arial", 24, [System.Drawing.FontStyle]::Bold)
$fontWatermark = New-Object System.Drawing.Font("Arial", 18, [System.Drawing.FontStyle]::Regular)

$penBorder = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(40, 40, 40), 10)
$penStick = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(20, 20, 20), 12)
$penThin = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(30, 30, 30), 6)
$penAccentCrimson = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 40, 40), 8)
$penAccentEmerald = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(30, 150, 60), 8)
$penAccentGold = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(240, 180, 20), 8)
$penAccentCyan = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(0, 180, 220), 6)

$brushDark = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(20, 20, 20))
$brushWhite = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$brushCrimson = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 40, 40))
$brushEmerald = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(30, 150, 60))
$brushGold = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(245, 190, 25))
$brushCyan = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(0, 180, 220))
$brushGrey = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(240, 240, 240))
$brushTextGrey = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(120, 120, 120))

$formatCenter = New-Object System.Drawing.StringFormat
$formatCenter.Alignment = [System.Drawing.StringAlignment]::Center
$formatCenter.LineAlignment = [System.Drawing.StringAlignment]::Center

function Draw-Everyman {
    param($g, [int]$x, [int]$y, [string]$pose = "standing")
    
    # Head
    $headSize = 130
    $headX = $x - 65
    $headY = $y - 320
    $g.FillEllipse($brushDark, $headX, $headY, $headSize, $headSize)
    
    # Expressive white eyes & dark pupils
    $g.FillEllipse($brushWhite, ($x - 26), ($headY + 45), 18, 22)
    $g.FillEllipse($brushWhite, ($x + 8), ($headY + 45), 18, 22)
    $g.FillEllipse($brushDark, ($x - 20), ($headY + 50), 8, 12)
    $g.FillEllipse($brushDark, ($x + 14), ($headY + 50), 8, 12)

    # Torso (White collared shirt)
    $g.FillRectangle($brushWhite, ($x - 50), ($y - 180), 100, 180)
    $g.DrawRectangle($penStick, ($x - 50), ($y - 180), 100, 180)

    # Collar lines
    $g.DrawLine($penThin, ($x - 30), ($y - 180), ($x - 5), ($y - 150))
    $g.DrawLine($penThin, ($x + 30), ($y - 180), ($x + 5), ($y - 150))

    # Thin black necktie
    $g.FillRectangle($brushDark, ($x - 10), ($y - 165), 20, 120)

    # Arms & Legs based on pose
    if ($pose -eq "shrugging" -or $pose -eq "calm") {
        # Relaxed arms / hands in pockets
        $g.DrawLine($penStick, ($x - 50), ($y - 170), ($x - 90), ($y - 80))
        $g.DrawLine($penStick, ($x - 90), ($y - 80), ($x - 40), ($y - 20))
        $g.DrawLine($penStick, ($x + 50), ($y - 170), ($x + 90), ($y - 80))
        $g.DrawLine($penStick, ($x + 90), ($y - 80), ($x + 40), ($y - 20))
        # Legs
        $g.DrawLine($penStick, ($x - 30), ($y), ($x - 35), ($y + 180))
        $g.DrawLine($penStick, ($x + 30), ($y), ($x + 35), ($y + 180))
    }
    elseif ($pose -eq "panicked") {
        # Hands on head
        $g.DrawLine($penStick, ($x - 50), ($y - 170), ($x - 90), ($y - 250))
        $g.DrawLine($penStick, ($x - 90), ($y - 250), ($x - 40), ($y - 270))
        $g.DrawLine($penStick, ($x + 50), ($y - 170), ($x + 90), ($y - 250))
        $g.DrawLine($penStick, ($x + 90), ($y - 250), ($x + 40), ($y - 270))
        # Legs
        $g.DrawLine($penStick, ($x - 30), ($y), ($x - 55), ($y + 180))
        $g.DrawLine($penStick, ($x + 30), ($y), ($x + 55), ($y + 180))
    }
    elseif ($pose -eq "walking") {
        # Walking forward confidently
        $g.DrawLine($penStick, ($x - 50), ($y - 170), ($x - 95), ($y - 80))
        $g.DrawLine($penStick, ($x + 50), ($y - 170), ($x + 85), ($y - 110))
        # Legs stride
        $g.DrawLine($penStick, ($x - 30), ($y), ($x - 65), ($y + 180))
        $g.DrawLine($penStick, ($x + 30), ($y), ($x + 60), ($y + 170))
    }
    else {
        # Standard confident
        $g.DrawLine($penStick, ($x - 50), ($y - 170), ($x - 85), ($y - 60))
        $g.DrawLine($penStick, ($x + 50), ($y - 170), ($x + 85), ($y - 60))
        $g.DrawLine($penStick, ($x - 30), ($y), ($x - 35), ($y + 180))
        $g.DrawLine($penStick, ($x + 30), ($y), ($x + 35), ($y + 180))
    }
}

$sceneIndex = 0
foreach ($sc in $scenes) {
    $sceneIndex++
    $bmp = New-Object System.Drawing.Bitmap 1080, 1920
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    
    # Background - Crisp StickLit Paper
    $g.Clear([System.Drawing.Color]::FromArgb(252, 252, 252))
    
    # Outer Framing Box
    $g.DrawRectangle($penBorder, 30, 30, 1020, 1860)
    
    # Top Watermark
    $watermarkText = "BOOK-2MIN  *  STICKLIT ANIMATED SUMMARY  *  SCENE $($sceneIndex.ToString('D2'))/24"
    $g.DrawString($watermarkText, $fontWatermark, $brushTextGrey, (New-Object System.Drawing.RectangleF(50, 70, 980, 40)), $formatCenter)
    
    # Big Bold Top Headline Banner
    $headline = $sc.headline.ToUpper()
    
    # Headline drop-shadow block
    $g.FillRectangle($brushDark, 70, 140, 940, 120)
    $g.FillRectangle($brushWhite, 64, 134, 940, 120)
    $g.DrawRectangle($penStick, 64, 134, 940, 120)
    $g.DrawString($headline, $fontHeadline, $brushDark, (New-Object System.Drawing.RectangleF(64, 134, 940, 120)), $formatCenter)

    # Pill Callout Tags
    $tag1 = "[ " + $sc.tag_1.ToUpper() + " ]"
    $tag2 = "[ " + $sc.tag_2.ToUpper() + " ]"

    # Pill 1
    $g.FillRectangle($brushCrimson, 100, 280, 420, 56)
    $g.DrawRectangle($penStick, 100, 280, 420, 56)
    $g.DrawString($tag1, $fontTag, $brushWhite, (New-Object System.Drawing.RectangleF(100, 280, 420, 56)), $formatCenter)

    # Pill 2
    $g.FillRectangle($brushGold, 560, 280, 420, 56)
    $g.DrawRectangle($penStick, 560, 280, 420, 56)
    $g.DrawString($tag2, $fontTag, $brushDark, (New-Object System.Drawing.RectangleF(560, 280, 420, 56)), $formatCenter)

    # Central Illustration Stage
    $centerX = 540
    $stageY = 1100

    # Ground line
    $g.DrawLine($penStick, 120, ($stageY + 180), 960, ($stageY + 180))
    
    # Specific props and Everyman action per scene
    switch ($sc.id) {
        1 {
            # Calm in chaos
            Draw-Everyman $g $centerX $stageY "calm"
            for ($a = 0; $a -lt 6; $a++) {
                $ax = 200 + ($a * 130)
                $ay = 650 + (($a % 3) * 70)
                $g.DrawLine($penAccentCrimson, $ax, $ay, ($ax + 80), ($ay + 40))
            }
        }
        2 {
            # Billboards crushing down
            Draw-Everyman $g $centerX $stageY "panicked"
            $g.FillRectangle($brushCyan, 160, 540, 360, 100)
            $g.DrawRectangle($penStick, 160, 540, 360, 100)
            $g.DrawString("BE HAPPIER!", $fontSub, $brushDark, (New-Object System.Drawing.RectangleF(160, 540, 360, 100)), $formatCenter)
            $g.FillRectangle($brushGold, 560, 500, 360, 100)
            $g.DrawRectangle($penStick, 560, 500, 360, 100)
            $g.DrawString("BE RICHER!", $fontSub, $brushDark, (New-Object System.Drawing.RectangleF(560, 500, 360, 100)), $formatCenter)
        }
        3 {
            # Feedback loop spiral
            Draw-Everyman $g $centerX $stageY "panicked"
            for ($r = 150; $r -lt 360; $r += 50) {
                $g.DrawEllipse($penAccentCrimson, ($centerX - $r), ($stageY - 260 - $r), ($r * 2), ($r * 2))
            }
            # Sweat drops
            $g.FillEllipse($brushCyan, ($centerX - 100), ($stageY - 330), 20, 30)
            $g.FillEllipse($brushCyan, ($centerX + 80), ($stageY - 340), 20, 30)
        }
        4 {
            # Fake smile in mirror
            Draw-Everyman $g ($centerX - 140) $stageY "standing"
            $g.DrawRectangle($penStick, ($centerX + 40), ($stageY - 350), 260, 500)
            $g.FillRectangle($brushGrey, ($centerX + 50), ($stageY - 340), 240, 480)
            # Giant smiley face
            $g.FillEllipse($brushGold, ($centerX + 110), ($stageY - 250), 120, 120)
            $g.DrawEllipse($penStick, ($centerX + 110), ($stageY - 250), 120, 120)
        }
        5 {
            # Golden crown
            Draw-Everyman $g $centerX ($stageY - 80) "standing"
            $g.FillRectangle($brushGold, ($centerX - 60), ($stageY - 400), 120, 70)
            $g.DrawRectangle($penStick, ($centerX - 60), ($stageY - 400), 120, 70)
        }
        6 {
            # Balance scale
            $g.DrawLine($penStick, $centerX, ($stageY + 180), $centerX, ($stageY - 100))
            $g.DrawLine($penStick, ($centerX - 280), ($stageY - 80), ($centerX + 280), ($stageY - 120))
            $g.FillEllipse($brushCrimson, ($centerX - 320), ($stageY - 70), 80, 80)
            $g.FillEllipse($brushEmerald, ($centerX + 240), ($stageY - 160), 80, 80)
            Draw-Everyman $g $centerX $stageY "shrugging"
        }
        7 {
            # Umbrella in rain
            Draw-Everyman $g $centerX $stageY "standing"
            $g.FillPie($brushEmerald, ($centerX - 170), ($stageY - 480), 340, 240, 180, 180)
            $g.DrawArc($penStick, ($centerX - 170), ($stageY - 480), 340, 240, 180, 180)
            $g.DrawLine($penStick, $centerX, ($stageY - 360), $centerX, ($stageY - 140))
            for ($rn = 0; $rn -lt 12; $rn++) {
                $rx = 180 + ($rn * 65)
                $ry = 450 + (($rn % 4) * 60)
                $g.DrawLine($penAccentCyan, $rx, $ry, ($rx + 10), ($ry + 45))
            }
        }
        8 {
            # Bunker
            $g.FillRectangle($brushDark, 300, ($stageY - 150), 480, 330)
            $g.DrawRectangle($penBorder, 300, ($stageY - 150), 480, 330)
            $g.DrawString("TERRIFIED OF LIFE", $fontSub, $brushWhite, (New-Object System.Drawing.RectangleF(300, ($stageY - 80), 480, 100)), $formatCenter)
        }
        9 {
            # Walking right
            Draw-Everyman $g ($centerX + 120) $stageY "walking"
            $g.DrawLine($penAccentEmerald, 200, 680, 880, 680)
        }
        10 {
            # Finite Fucks Jar
            Draw-Everyman $g ($centerX - 180) $stageY "shrugging"
            $jarX = $centerX + 100
            $jarY = $stageY - 200
            $g.DrawRectangle($penStick, $jarX, $jarY, 220, 340)
            $g.DrawString("FUCKS", $fontSub, $brushDark, (New-Object System.Drawing.RectangleF($jarX, ($jarY + 30), 220, 60)), $formatCenter)
            $g.FillEllipse($brushGold, ($jarX + 50), ($jarY + 230), 50, 50)
            $g.DrawEllipse($penStick, ($jarX + 50), ($jarY + 230), 50, 50)
            $g.FillEllipse($brushGold, ($jarX + 110), ($jarY + 240), 50, 50)
            $g.DrawEllipse($penStick, ($jarX + 110), ($jarY + 240), 50, 50)
        }
        11 {
            # Trivial mosquitoes
            Draw-Everyman $g $centerX $stageY "panicked"
            $bugs = @("SLOW WIFI", "RUDE CASHIER", "TRAFFIC", "BAD WEATHER")
            for ($b = 0; $b -lt $bugs.Count; $b++) {
                $bx = 160 + (($b % 2) * 580)
                $by = 640 + ([int]($b / 2) * 160)
                $g.FillEllipse($brushCrimson, $bx, $by, 60, 40)
                $g.DrawString($bugs[$b], $fontSub, $brushDark, ($bx - 20), ($by - 40))
            }
        }
        12 {
            # Two Pillars
            $g.FillRectangle($brushCrimson, 200, ($stageY - 320), 160, 500)
            $g.DrawRectangle($penStick, 200, ($stageY - 320), 160, 500)
            $g.DrawString("BAD`nVALUES", $fontSub, $brushWhite, (New-Object System.Drawing.RectangleF(200, ($stageY - 200), 160, 200)), $formatCenter)

            $g.FillRectangle($brushEmerald, 720, ($stageY - 320), 160, 500)
            $g.DrawRectangle($penStick, 720, ($stageY - 320), 160, 500)
            $g.DrawString("GOOD`nVALUES", $fontSub, $brushWhite, (New-Object System.Drawing.RectangleF(720, ($stageY - 200), 160, 200)), $formatCenter)
            Draw-Everyman $g $centerX $stageY "standing"
        }
        13 {
            # Puppet strings
            Draw-Everyman $g $centerX $stageY "panicked"
            $g.DrawLine($penAccentCrimson, 300, 480, ($centerX - 80), ($stageY - 200))
            $g.DrawLine($penAccentCrimson, 780, 480, ($centerX + 80), ($stageY - 200))
            $g.DrawString("SOCIAL APPROVAL", $fontSub, $brushCrimson, 180, 440)
            $g.DrawString("ALWAYS RIGHT", $fontSub, $brushCrimson, 680, 440)
        }
        14 {
            # Compass
            Draw-Everyman $g $centerX $stageY "standing"
            $compX = $centerX
            $compY = $stageY - 80
            $g.FillEllipse($brushEmerald, ($compX - 60), ($compY - 60), 120, 120)
            $g.DrawEllipse($penBorder, ($compX - 60), ($compY - 60), 120, 120)
            $g.DrawLine($penStick, $compX, ($compY + 40), $compX, ($compY - 50))
            $g.DrawString("N", $fontSub, $brushWhite, ($compX - 12), ($compY - 45))
        }
        15 {
            # Mountain
            Draw-Everyman $g ($centerX + 100) ($stageY - 140) "walking"
            $g.DrawLine($penStick, 120, ($stageY + 180), 700, ($stageY - 340))
            $g.DrawLine($penStick, 700, ($stageY - 340), 960, ($stageY + 180))
        }
        16 {
            # Wrench
            Draw-Everyman $g ($centerX - 80) $stageY "standing"
            $g.FillRectangle($brushCyan, ($centerX + 80), ($stageY - 100), 220, 60)
            $g.DrawRectangle($penStick, ($centerX + 80), ($stageY - 100), 220, 60)
            $g.DrawLine($penStick, ($centerX - 40), ($stageY - 80), ($centerX + 120), ($stageY - 80))
        }
        17 {
            # Upgrade problems
            Draw-Everyman $g $centerX $stageY "standing"
            $g.DrawLine($penAccentEmerald, 240, ($stageY - 20), 840, ($stageY - 260))
            $g.DrawString("BETTER PROBLEMS", $fontHeadline, $brushEmerald, (New-Object System.Drawing.RectangleF(200, 650, 680, 100)), $formatCenter)
        }
        18 {
            # Hourglass
            Draw-Everyman $g ($centerX - 160) $stageY "panicked"
            $hgX = $centerX + 140
            $hgY = $stageY - 240
            $g.FillRectangle($brushGold, ($hgX - 70), $hgY, 140, 200)
            $g.DrawRectangle($penStick, ($hgX - 70), $hgY, 140, 200)
        }
        19 {
            # Do something kinetic loop
            Draw-Everyman $g $centerX $stageY "standing"
            $g.DrawArc($penAccentGold, 260, 520, 560, 400, 0, 360)
            $g.DrawString("ACTION -> INSPIRATION -> MOTIVATION", $fontSub, $brushDark, (New-Object System.Drawing.RectangleF(100, 480, 880, 60)), $formatCenter)
        }
        20 {
            # Single chalk step
            Draw-Everyman $g ($centerX - 60) $stageY "walking"
            $g.DrawLine($penAccentEmerald, 200, ($stageY + 180), 880, ($stageY + 180))
            $g.DrawString("START SMALL", $fontHeadline, $brushEmerald, (New-Object System.Drawing.RectangleF(200, 680, 680, 100)), $formatCenter)
        }
        21 {
            # Memento Mori Skull
            Draw-Everyman $g ($centerX - 100) $stageY "standing"
            $skX = $centerX + 140
            $skY = $stageY - 140
            $g.FillEllipse($brushWhite, $skX, $skY, 130, 130)
            $g.DrawEllipse($penStick, $skX, $skY, 130, 130)
            $g.FillEllipse($brushDark, ($skX + 25), ($skY + 45), 25, 25)
            $g.FillEllipse($brushDark, ($skX + 75), ($skY + 45), 25, 25)
            $g.DrawLine($penStick, ($skX + 65), ($skY + 70), ($skX + 65), ($skY + 95))
        }
        22 {
            # Stripping noise
            Draw-Everyman $g ($centerX - 160) $stageY "standing"
            for ($nf = 0; $nf -lt 6; $nf++) {
                $nx = 440 + ($nf * 80)
                $ny = 660 + (($nf % 3) * 80)
                $g.FillRectangle($brushCrimson, $nx, $ny, 90, 50)
                $g.DrawRectangle($penStick, $nx, $ny, 90, 50)
            }
        }
        23 {
            # 3 Pillars
            $pillars = @("INTEGRITY", "CRAFT", "LOVED ONES")
            for ($pl = 0; $pl -lt 3; $pl++) {
                $px = 160 + ($pl * 280)
                $g.FillRectangle($brushEmerald, $px, ($stageY - 260), 180, 440)
                $g.DrawRectangle($penStick, $px, ($stageY - 260), 180, 440)
                $g.DrawString($pillars[$pl], $fontSub, $brushWhite, (New-Object System.Drawing.RectangleF($px, ($stageY - 120), 180, 100)), $formatCenter)
            }
        }
        24 {
            # Sunrise horizon
            $g.FillPie($brushGold, ($centerX - 240), ($stageY - 80), 480, 400, 180, 180)
            $g.DrawArc($penStick, ($centerX - 240), ($stageY - 80), 480, 400, 180, 180)
            Draw-Everyman $g $centerX $stageY "standing"
        }
        default {
            Draw-Everyman $g $centerX $stageY "standing"
        }
    }

    # Bottom watermark signature
    $g.DrawString("@sticklit  *  HIGH-RETENTION ANIMATED SUMMARY", $fontWatermark, $brushTextGrey, (New-Object System.Drawing.RectangleF(50, 1800, 980, 40)), $formatCenter)

    $outImg = Join-Path $outputDir ("scene_{0:D2}.png" -f $sceneIndex)
    $bmp.Save($outImg, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Output "Rendered $outImg"
}

Write-Output "All 24 StickLit scene images successfully rendered!"
