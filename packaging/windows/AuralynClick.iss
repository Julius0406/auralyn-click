#ifndef MyAppVersion
#define MyAppVersion "2.4.1"
#endif
#ifndef SourceRoot
#define SourceRoot "."
#endif

#define MyAppName "Auralyn Click"
#define MyAppExeName "AuralynClick.exe"

[Setup]
AppId={{E46228BE-B314-4D11-9C45-BD749D0FA23F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Julius0406
DefaultDirName={localappdata}\Programs\Auralyn Click
DefaultGroupName=Auralyn Click
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir={#SourceRoot}\release
OutputBaseFilename=AuralynClick-{#MyAppVersion}-Windows-x64-Setup
SetupIconFile={#SourceRoot}\assets\auralyn-click.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no

[Files]
Source: "{#SourceRoot}\dist\AuralynClick\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked
Name: "autostart"; Description: "Start Auralyn Click when I sign in"; GroupDescription: "Startup:"; Flags: unchecked

[Icons]
Name: "{autoprograms}\Auralyn Click"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\Auralyn Click Setup"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--setup"
Name: "{autodesktop}\Auralyn Click"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "AuralynClick"; ValueData: "\"{app}\{#MyAppExeName}\" --show"; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Auralyn Click"; Flags: nowait postinstall skipifsilent

[Code]
var
  PersonalizePage: TWizardPage;
  StartupPage: TWizardPage;
  LanguageCombo: TNewComboBox;
  ThemeCombo: TNewComboBox;
  AccentCombo: TNewComboBox;
  BackgroundCombo: TNewComboBox;
  FpsCombo: TNewComboBox;
  StartupCombo: TNewComboBox;
  AnimationsCheck: TNewCheckBox;

procedure AddLabel(Page: TWizardPage; Caption: String; TopPos: Integer);
var
  L: TNewStaticText;
begin
  L := TNewStaticText.Create(Page);
  L.Parent := Page.Surface;
  L.Caption := Caption;
  L.Left := 0;
  L.Top := TopPos;
end;

function NewCombo(Page: TWizardPage; TopPos: Integer): TNewComboBox;
begin
  Result := TNewComboBox.Create(Page);
  Result.Parent := Page.Surface;
  Result.Left := 0;
  Result.Top := TopPos;
  Result.Width := Page.SurfaceWidth;
  Result.Style := csDropDownList;
end;

procedure InitializeWizard;
begin
  PersonalizePage := CreateCustomPage(
    wpSelectDir,
    'Personalize Auralyn Click',
    'Choose the default language and look. You can change all of this later.'
  );

  AddLabel(PersonalizePage, 'Language', 8);
  LanguageCombo := NewCombo(PersonalizePage, 28);
  LanguageCombo.Items.Add('System / Auto');
  LanguageCombo.Items.Add('Deutsch');
  LanguageCombo.Items.Add('English');
  LanguageCombo.Items.Add('Français');
  LanguageCombo.Items.Add('Español');
  LanguageCombo.Items.Add('Italiano');
  LanguageCombo.Items.Add('Português');
  LanguageCombo.Items.Add('Nederlands');
  LanguageCombo.Items.Add('Polski');
  LanguageCombo.Items.Add('Čeština');
  LanguageCombo.Items.Add('Slovenčina');
  LanguageCombo.Items.Add('Magyar');
  LanguageCombo.Items.Add('Română');
  LanguageCombo.Items.Add('Svenska');
  LanguageCombo.Items.Add('Norsk');
  LanguageCombo.Items.Add('Dansk');
  LanguageCombo.Items.Add('Suomi');
  LanguageCombo.Items.Add('Türkçe');
  LanguageCombo.Items.Add('Русский');
  LanguageCombo.Items.Add('Українська');
  LanguageCombo.Items.Add('Ελληνικά');
  LanguageCombo.Items.Add('日本語');
  LanguageCombo.Items.Add('한국어');
  LanguageCombo.Items.Add('中文');
  LanguageCombo.Items.Add('العربية');
  LanguageCombo.ItemIndex := 0;

  AddLabel(PersonalizePage, 'Theme', 68);
  ThemeCombo := NewCombo(PersonalizePage, 88);
  ThemeCombo.Items.Add('Midnight');
  ThemeCombo.Items.Add('AMOLED');
  ThemeCombo.Items.Add('Light');
  ThemeCombo.ItemIndex := 0;

  AddLabel(PersonalizePage, 'Accent', 128);
  AccentCombo := NewCombo(PersonalizePage, 148);
  AccentCombo.Items.Add('Violet');
  AccentCombo.Items.Add('Cyan');
  AccentCombo.Items.Add('Emerald');
  AccentCombo.Items.Add('Sunset');
  AccentCombo.Items.Add('Rose');
  AccentCombo.ItemIndex := 0;

  AddLabel(PersonalizePage, 'Background', 188);
  BackgroundCombo := NewCombo(PersonalizePage, 208);
  BackgroundCombo.Items.Add('Aurora');
  BackgroundCombo.Items.Add('Nebula');
  BackgroundCombo.Items.Add('Grid Waves');
  BackgroundCombo.Items.Add('Particles');
  BackgroundCombo.Items.Add('Static Gradient');
  BackgroundCombo.ItemIndex := 0;

  StartupPage := CreateCustomPage(
    PersonalizePage.ID,
    'Animation and startup',
    'Choose how much motion you want and what happens when Auralyn Click opens.'
  );

  AddLabel(StartupPage, 'Animated background FPS', 8);
  FpsCombo := NewCombo(StartupPage, 28);
  FpsCombo.Items.Add('30');
  FpsCombo.Items.Add('60');
  FpsCombo.Items.Add('120');
  FpsCombo.Items.Add('160');
  FpsCombo.ItemIndex := 1;

  AnimationsCheck := TNewCheckBox.Create(StartupPage);
  AnimationsCheck.Parent := StartupPage.Surface;
  AnimationsCheck.Caption := 'Enable animations';
  AnimationsCheck.Left := 0;
  AnimationsCheck.Top := 76;
  AnimationsCheck.Width := StartupPage.SurfaceWidth;
  AnimationsCheck.Checked := True;

  AddLabel(StartupPage, 'Start screen', 118);
  StartupCombo := NewCombo(StartupPage, 138);
  StartupCombo.Items.Add('Fullscreen');
  StartupCombo.Items.Add('Compact');
  StartupCombo.Items.Add('Off');
  StartupCombo.ItemIndex := 0;
end;

function SelectedLanguageCode: String;
begin
  case LanguageCombo.ItemIndex of
    1: Result := 'de';
    2: Result := 'en';
    3: Result := 'fr';
    4: Result := 'es';
    5: Result := 'it';
    6: Result := 'pt';
    7: Result := 'nl';
    8: Result := 'pl';
    9: Result := 'cs';
    10: Result := 'sk';
    11: Result := 'hu';
    12: Result := 'ro';
    13: Result := 'sv';
    14: Result := 'no';
    15: Result := 'da';
    16: Result := 'fi';
    17: Result := 'tr';
    18: Result := 'ru';
    19: Result := 'uk';
    20: Result := 'el';
    21: Result := 'ja';
    22: Result := 'ko';
    23: Result := 'zh';
    24: Result := 'ar';
  else
    Result := 'system';
  end;
end;

function SelectedStartupMode: String;
begin
  case StartupCombo.ItemIndex of
    1: Result := 'compact';
    2: Result := 'off';
  else
    Result := 'fullscreen';
  end;
end;

procedure WriteInitialSettings;
var
  SettingsDir: String;
  SettingsPath: String;
  Json: String;
  AnimationsText: String;
  AutostartText: String;
begin
  SettingsDir := ExpandConstant('{userappdata}\AuralynClick');
  SettingsPath := SettingsDir + '\settings.json';

  { Never overwrite an existing user's preferences during an upgrade. }
  if FileExists(SettingsPath) then
    exit;

  ForceDirectories(SettingsDir);

  if AnimationsCheck.Checked then
    AnimationsText := 'true'
  else
    AnimationsText := 'false';

  if WizardIsTaskSelected('autostart') then
    AutostartText := 'true'
  else
    AutostartText := 'false';

  Json := '{' + #13#10 +
    '  "language": "' + SelectedLanguageCode + '",' + #13#10 +
    '  "theme": "' + ThemeCombo.Text + '",' + #13#10 +
    '  "accent": "' + AccentCombo.Text + '",' + #13#10 +
    '  "background": "' + BackgroundCombo.Text + '",' + #13#10 +
    '  "background_fps": ' + FpsCombo.Text + ',' + #13#10 +
    '  "animations": ' + AnimationsText + ',' + #13#10 +
    '  "startup_screen": "' + SelectedStartupMode + '",' + #13#10 +
    '  "autostart": ' + AutostartText + ',' + #13#10 +
    '  "setup_completed": true' + #13#10 +
    '}';

  SaveStringToFile(SettingsPath, Json, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    WriteInitialSettings;
end;
