# Definér rotmappen for din Controllerhåndbok / Kunnskapsbase
$RootPath = "C:\Users\frank\Desktop\Controllerhandbok"

# Liste over mapper som skal opprettes basert på statlig økonomistyring og UH-sektoren
$Folders = @(
    "01_Overordnet_Regelverk_og_Styring\01.1_Statlig_Regelverk",
    "01_Overordnet_Regelverk_og_Styring\01.2_UH_Instrukser",
    "01_Overordnet_Regelverk_og_Styring\01.3_Interne_Hovedregler",
    
    "02_Fullmakter_Roller_og_Delegasjon\02.1_BDM_og_Fullmaktsmatrise",
    "02_Fullmakter_Roller_og_Delegasjon\02.2_Funksjonsskille_og_Attestasjon",
    "02_Fullmakter_Roller_og_Delegasjon\02.3_Habilitet_og_Etikk",
    
    "03_Budsjettering_og_Okonomioppfolging\03.1_Tildeling_og_Internfordeling",
    "03_Budsjettering_og_Okonomioppfolging\03.2_Manedlig_og_Tertialvis_Oppfolging",
    "03_Budsjettering_og_Okonomioppfolging\03.3_Avsetninger_og_Ubenyttede_Midler",
    
    "04_Regnskap_SRS_og_Kontoplan\04.1_Statens_Kontoplan",
    "04_Regnskap_SRS_og_Kontoplan\04.2_Regnskapsstandarder_SRS",
    "04_Regnskap_SRS_og_Kontoplan\04.3_Bokforing_og_Avstemming",
    "04_Regnskap_SRS_og_Kontoplan\04.4_Arsrapport_og_Arsregnskap",
    
    "05_Prosjektokonomi_og_BOA\05.1_Klassifisering_SRS9_SRS10",
    "05_Prosjektokonomi_og_BOA\05.2_Kalkyle_og_TDI_Modell",
    "05.3_Prosjektgjennomgang_og_Fakturering",
    "05.4_Prosjektslutt_og_Tapsavsetning",
    
    "06_Internkontroll_Risikostyring_og_Revisjon\06.1_Internkontrollrutiner",
    "06_Internkontroll_Risikostyring_og_Revisjon\06.2_Risikovurdering_og_Rapportering",
    "06_Internkontroll_Risikostyring_og_Revisjon\06.3_Misligheter_og_Revisjon"
)

# Opprett rotmappen og undermapper
foreach ($Folder in $Folders) {
    $FullPath = Join-Path $RootPath $Folder
    if (-not (Test-Path $FullPath)) {
        New-Item -ItemType Directory -Path $FullPath -Force | Out-Null
        Write-Host "Opprettet: $FullPath" -ForegroundColor Green
    } else {
        Write-Host "Eksisterer allerede: $FullPath" -ForegroundColor Yellow
    }
}

Write-Host "`nMappestrukturen for Controllerhåndboken er ferdig opprettet i $RootPath!" -ForegroundColor Cyan