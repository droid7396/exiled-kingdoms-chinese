# Exiled Kingdoms Chinese Patch - installer
# Requires: Windows 10/11 built-in PowerShell 5.1, Chinese Windows (SimHei)
param(
    [string]$GameDir = ""
)
$ErrorActionPreference = 'Stop'

$PatchDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExeName = 'exiledkingdoms.exe'
$BackupName = 'exiledkingdoms_en.exe'
$FONT_SIZES = @{ default=17; tahoma16white=16; tahoma20bold=20; tahoma20white=20;
 tahoma22bold=22; tahoma22outline=22; tahoma23white=23; tahoma24bold=24; tahoma25white=25;
 tahoma26bold=26; tahoma27bold=27; tahoma27outline=27; tahoma27white=27; tahoma31outline=31;
 tahoma32=32; tahoma32bold=32; tahoma38outline=38; arialnarrow40bold=40 }
Add-Type -AssemblyName 'System.IO.Compression'
Add-Type -AssemblyName 'System.IO.Compression.FileSystem'

function Die($msg) {
    Write-Host ('[错误] ' + $msg) -ForegroundColor Red
    Read-Host '按回车退出'
    exit 1
}

function Find-GameDir {
    $candidates = @(
        'C:\Program Files (x86)\Steam\steamapps\common\Exiled Kingdoms',
        'C:\Program Files\Steam\steamapps\common\Exiled Kingdoms',
        'D:\Steam\steamapps\common\Exiled Kingdoms',
        'D:\Program Files (x86)\Steam\steamapps\common\Exiled Kingdoms',
        'E:\Steam\steamapps\common\Exiled Kingdoms'
    )
    foreach ($d in $candidates) {
        if (Test-Path (Join-Path $d $ExeName)) { return $d }
    }
    $d = Read-Host '未自动找到游戏目录，请输入游戏安装目录（如 C:\Program Files (x86)\Steam\steamapps\common\Exiled Kingdoms）'
    $d = $d.Trim('"').Trim()
    if (-not (Test-Path (Join-Path $d $ExeName))) { Die ('目录下未找到 ' + $ExeName) }
    return $d
}

function Find-EOCD([byte[]]$bytes) {
    for ($i = $bytes.Length - 22; $i -ge $bytes.Length - 65557 -and $i -ge 0; $i--) {
        if ($bytes[$i] -eq 0x50 -and $bytes[$i+1] -eq 0x4B -and $bytes[$i+2] -eq 0x05 -and $bytes[$i+3] -eq 0x06) {
            return $i
        }
    }
    return -1
}

Write-Host '========================================================'
Write-Host '  Exiled Kingdoms 汉化补丁 v1.0 安装程序'
Write-Host '  适配：Steam 版 v1.3.1210 | 需中文 Windows'
Write-Host '========================================================'

# 定位游戏目录
if ($GameDir -ne '') {
    if (-not (Test-Path (Join-Path $GameDir $ExeName))) { Die ('指定目录下未找到 ' + $ExeName) }
} else {
    $GameDir = Find-GameDir
}
Write-Host ('游戏目录：' + $GameDir)

# 检测游戏进程
$procs = Get-Process -Name 'exiledkingdoms', 'javaw' -ErrorAction SilentlyContinue
if ($procs) { Die '检测到游戏正在运行，请先完全退出游戏再运行本补丁。' }

function Uninstall-Patch([string]$dir) {
    Write-Host '卸载汉化（还原英文原版）...'
    $exePath2 = Join-Path $dir $ExeName
    $bak = Join-Path $dir $BackupName
    if (-not (Test-Path $bak)) { Die '未找到原版备份 ' + $BackupName + '，无法卸载。' }
    # 删除补丁部署的目录
    $dirs = @('data\conversations\RU', 'data\quests\RU', 'data\quests\variations',
              'data\rules\RU', 'data\ui\fonts', 'data\ui\strings')
    foreach ($d in $dirs) {
        $p = Join-Path $dir $d
        if (Test-Path $p) { Remove-Item $p -Recurse -Force }
    }
    # 删除补丁部署的文件
    $files = @('data\rules\items_text.txt', 'data\rules\bestiary_names.txt',
               'data\world\castles_desc.txt', 'data\world\factions_text.txt',
               'data\world\random_names.txt', 'data\world\areas.txt',
               'data\world\castles.txt', 'data\world\event_locations.txt',
               'data\world\regions.txt', 'data\world\rumors.txt')
    foreach ($f in $files) {
        $p = Join-Path $dir $f
        if (Test-Path $p) { Remove-Item $p -Force }
    }
    # 还原 exe 并删除备份（完全还原原版状态）
    Copy-Item $bak $exePath2 -Force
    Remove-Item $bak -Force
    Write-Host '已还原英文原版并删除备份。卸载完成。'
}

# 操作选择
Write-Host ''
Write-Host '请选择操作：'
Write-Host '  [1] 安装汉化（默认）'
Write-Host '  [2] 卸载汉化（还原英文原版）'
$choice = Read-Host '输入 1 或 2 后回车'
if ($choice -eq '2') {
    Uninstall-Patch $GameDir
    Read-Host '卸载完成，按回车退出'
    exit 0
}

$exePath = Join-Path $GameDir $ExeName


$exePath = Join-Path $GameDir $ExeName

# 1) 备份
$backupPath = Join-Path $GameDir $BackupName
if (-not (Test-Path $backupPath)) {
    Write-Host ('备份原版 exe -> ' + $BackupName)
    Copy-Item $exePath $backupPath
} else {
    Write-Host '已存在原版备份，跳过备份。'
}

# 2) 读取 exe 头部与尾部，定位内嵌 jar（流式，不整读大文件）
$fileLen = (Get-Item $exePath).Length
$fs = [IO.File]::OpenRead($exePath)
$head = New-Object byte[] 418400
[void]$fs.Read($head, 0, $head.Length)
$tailLen = 65557
$tail = New-Object byte[] $tailLen
$fs.Seek(-$tailLen, 'End') | Out-Null
[void]$fs.Read($tail, 0, $tailLen)
$fs.Dispose()
$eocd = -1
for ($i = $tailLen - 22; $i -ge 0; $i--) {
    if ($tail[$i] -eq 0x50 -and $tail[$i+1] -eq 0x4B -and $tail[$i+2] -eq 0x05 -and $tail[$i+3] -eq 0x06) {
        $eocd = $fileLen - $tailLen + $i
        break
    }
}
if ($eocd -lt 0) { Die 'exe 内未找到 zip 结构，文件可能不是原版 v1.3.1210。' }
$cdSize = [BitConverter]::ToInt32($tail, $i + 12)
$cdOff  = [BitConverter]::ToInt32($tail, $i + 16)
$jarStart = $eocd - $cdSize - $cdOff
if ($jarStart -lt 0 -or $jarStart -ge $fileLen) { Die '内嵌 jar 偏移计算异常。' }
Write-Host ('内嵌 jar 起始偏移：' + $jarStart)

# 3) 提取内嵌 jar 到临时文件 -> ZipArchive 更新模式替换补丁 class（全流式）
$patchJarPath = Join-Path $PatchDir 'patch_classes.jar'
if (-not (Test-Path $patchJarPath)) { Die '缺少 patch_classes.jar（补丁包不完整）。' }
$tmpJar = Join-Path $env:TEMP 'ek_game_jar.bin'
$in = [IO.File]::OpenRead($exePath)
$in.Seek($jarStart, 'Begin') | Out-Null
$out = [IO.File]::Create($tmpJar)
$in.CopyTo($out)
$out.Dispose(); $in.Dispose()
$jarArch = [IO.Compression.ZipFile]::Open($tmpJar, [System.IO.Compression.ZipArchiveMode]::Update)
$patchArch = [IO.Compression.ZipFile]::OpenRead($patchJarPath)
$patchMap = @{}
foreach ($e in $patchArch.Entries) {
    if ($e.FullName.EndsWith('.class')) {
        $ms2 = New-Object System.IO.MemoryStream
        $e.Open().CopyTo($ms2)
        $patchMap[$e.FullName] = $ms2.ToArray()
        $ms2.Dispose()
    }
}
$patchArch.Dispose()
$replaced = 0
$toReplace = @('net/fdgames/UI/a/ae.class','net/fdgames/UI/a/F.class',
 'net/fdgames/UI/MainMenu/BackupWindow.class','net/fdgames/Helpers/FDUtils.class',
 'net/fdgames/GameEntities/Character.class','net/fdgames/Rules/SkillActions.class',
 'net/fdgames/GameEntities/Helpers/BestiaryData.class')
foreach ($name in $toReplace) {
    $entry = $jarArch.GetEntry($name)
    if ($null -eq $entry) { Die ('补丁目标未在 jar 中找到：' + $name) }
    $entry.Delete()
    $newEntry = $jarArch.CreateEntry($name)
    $ws = $newEntry.Open()
    $ws.Write($patchMap[$name], 0, $patchMap[$name].Length)
    $ws.Dispose()
    $replaced++
}
$jarArch.Dispose()
Write-Host ('已替换补丁 class：' + $replaced + ' 个')

# 4) 写回 exe：壳字节 + 修改后的 jar 文件（流式复制）
$shell = [IO.File]::ReadAllBytes($exePath)
if ($shell.Length -lt $jarStart) { Die 'exe 读取异常。' }
$outExe = [IO.File]::Create($exePath)
$outExe.Write($shell, 0, $jarStart)
$jin = [IO.File]::OpenRead($tmpJar)
$jin.CopyTo($outExe)
$jin.Dispose()
$outExe.Dispose()
Remove-Item $tmpJar -Force
Write-Host '汉化 exe 写回完成。'

# 5) 部署数据叠加包
$dataZip = Join-Path $PatchDir 'data.zip'
if (-not (Test-Path $dataZip)) { Die '缺少 data.zip（补丁包不完整）。' }
Write-Host '部署汉化数据...'
Expand-Archive -Path $dataZip -DestinationPath $GameDir -Force

# 6) 生成本机字体
$toolkit = Join-Path $PatchDir 'fontbm_toolkit'
$fontbm = Join-Path $toolkit 'fontbm.exe'
$chars = Join-Path $toolkit 'chars_all.txt'
$simhei = Join-Path $env:SystemRoot 'Fonts\simhei.ttf'
if (-not (Test-Path $simhei)) { Die ('未找到本机中易黑体（' + $simhei + '），本补丁依赖中文 Windows 自带字体。') }
if (-not (Test-Path $fontbm)) { Die '缺少 fontbm.exe（补丁包不完整）。' }
$outFonts = Join-Path $GameDir 'data\ui\fonts'
New-Item -ItemType Directory -Force -Path $outFonts | Out-Null
$genRoot = Join-Path $env:TEMP ('ek_font_' + [guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Force -Path $genRoot | Out-Null
Write-Host '生成中文字体（首次约 8-10 分钟，请耐心等待；已生成的档位自动跳过）...'
foreach ($name in $FONT_SIZES.Keys) {
    $size = $FONT_SIZES[$name]
    $outFnt = Join-Path $outFonts ($name + '.fnt')
    $outPng = Join-Path $outFonts ($name + '_0.png')
    if ((Test-Path $outFnt) -and (Test-Path $outPng)) {
        Write-Host ('  跳过 ' + $name + '（已存在）')
        continue
    }
    Write-Host ('  生成 ' + $name + ' (' + $size + 'px)...')
    & $fontbm --font-file $simhei --font-size $size --chars-file $chars `
        --output (Join-Path $genRoot ('size' + $size)) --data-format txt `
        --texture-size '2048x2048,4096x4096' 2>&1 | Out-Null
    $genFnt = Join-Path $genRoot ('size' + $size + '.fnt')
    $genPng = Join-Path $genRoot ('size' + $size + '_0.png')
    if (-not (Test-Path $genFnt)) { Die ('字体生成失败：' + $name) }
    # 派生：改名 + CRLF
    $t = [IO.File]::ReadAllText($genFnt).Replace('size' + $size + '_', $name + '_')
    [IO.File]::WriteAllText((Join-Path $outFonts ($name + '.fnt')), $t.Replace("`r`n", "`n").Replace("`n", "`r`n"))
    Copy-Item $genPng (Join-Path $outFonts ($name + '_0.png')) -Force
}
Remove-Item $genRoot -Recurse -Force -ErrorAction SilentlyContinue
Write-Host '字体生成完成（18 档）。'

# 7) 校验（exe 的 zip 尾部 EOCD 已在步骤 2 定位成功 = 结构完整；此处校验数据文件）
$z = [IO.Compression.ZipFile]::OpenRead($exePath)
$cnt = $z.Entries.Count
$z.Dispose()
Write-Host ('exe 条目计数（.NET 对带前缀 zip 可能少计，仅供参考）：' + $cnt)
foreach ($f in @('data\conversations\RU\adaon_tutorial.txt','data\world\random_names.txt',
                 'data\ui\fonts\tahoma23white.fnt','data\ui\fonts\tahoma23white_0.png',
                 'data\rules\RU\skills.txt','data\world\factions_text.txt')) {
    if (-not (Test-Path (Join-Path $GameDir $f))) { Die ('缺少 ' + $f) }
}

Write-Host '========================================================'
Write-Host '  安装完成！'
Write-Host '  1. 从 Steam 库启动游戏'
Write-Host '  2. Options -> Language -> Русский（俄语）-> 界面即为中文'
Write-Host '  3. Steam 提示文件不一致点取消；'
Write-Host '     「验证完整性」还原英文后，重跑本脚本即可恢复中文'
Write-Host '  卸载：删除 data 下补丁目录，'
Write-Host '        用 exiledkingdoms_en.exe 覆盖回 exiledkingdoms.exe'
Write-Host '========================================================'
Read-Host '按回车退出'
