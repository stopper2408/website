$baseUrl = "https://raw.githubusercontent.com/BinBashBanana/gfiles/master/gfiles/html5/hextris/"
$targetDir = "games\hextris"

New-Item -ItemType Directory -Force -Path "$targetDir\style"
New-Item -ItemType Directory -Force -Path "$targetDir\vendor"
New-Item -ItemType Directory -Force -Path "$targetDir\js"

$files = @(
    "index.html",
    "style/style.css",
    "vendor/hammer.min.js",
    "vendor/js.cookie.js",
    "vendor/jsonfn.min.js",
    "vendor/keypress.min.js",
    "vendor/jquery.js",
    "js/save-state.js",
    "js/view.js",
    "js/wavegen.js",
    "js/math.js",
    "js/Block.js",
    "js/Hex.js",
    "js/Text.js",
    "js/main.js",
    "js/game.js"
)

foreach ($file in $files) {
    $url = $baseUrl + $file
    $output = "$targetDir\$($file.Replace('/', '\'))"
    Write-Host "Downloading $file..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $output
    } catch {
        Write-Host "Failed to download $file"
    }
}

# Cookie Clicker
$ccBaseUrl = "https://raw.githubusercontent.com/BinBashBanana/gfiles/master/gfiles/html5/cookieclicker/"
$ccTargetDir = "games\cookieclicker"

New-Item -ItemType Directory -Force -Path "$ccTargetDir\img"
New-Item -ItemType Directory -Force -Path "$ccTargetDir\snd"

$ccFiles = @(
    "index.html",
    "style.css",
    "main.js",
    "base64.js",
    "img/darkNoise.jpg",
    "img/shadedBorders.png",
    "img/panelBG.png",
    "img/panelVertical.png",
    "img/panelGradientTop.png",
    "img/panelGradientBottom.png",
    "img/smallCookies.png",
    "img/perfectCookie.png",
    "img/imperfectCookie.png",
    "img/goldCookie.png",
    "img/cursor.png",
    "img/icons.png"
)

foreach ($file in $ccFiles) {
    $url = $ccBaseUrl + $file
    $output = "$ccTargetDir\$($file.Replace('/', '\'))"
    Write-Host "Downloading $file..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $output
    } catch {
        Write-Host "Failed to download $file"
    }
}
