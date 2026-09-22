#!/usr/bin/env python3
"""
Injects the AdMob App ID into the freshly generated Android project.

Run this after `npx cap add android` and before `npx cap sync android`.
It is safe to run more than once — it skips changes that are already present.
"""
import re

ADMOB_APP_ID = "ca-app-pub-1575997980091765~7586477365"

strings_path = "android/app/src/main/res/values/strings.xml"
with open(strings_path, "r", encoding="utf-8") as f:
    strings_xml = f.read()

if "admob_app_id" not in strings_xml:
    strings_xml = strings_xml.replace(
        "</resources>",
        f'    <string name="admob_app_id">{ADMOB_APP_ID}</string>\n</resources>'
    )
    with open(strings_path, "w", encoding="utf-8") as f:
        f.write(strings_xml)
    print(f"Added admob_app_id string to {strings_path}")
else:
    print(f"admob_app_id already present in {strings_path}, skipping")

manifest_path = "android/app/src/main/AndroidManifest.xml"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest_xml = f.read()

if "com.google.android.gms.ads.APPLICATION_ID" not in manifest_xml:
    meta_data = (
        '\n    <meta-data\n'
        '        android:name="com.google.android.gms.ads.APPLICATION_ID"\n'
        '        android:value="@string/admob_app_id"/>'
    )
    manifest_xml = re.sub(r'(<application[^>]*>)', r'\1' + meta_data, manifest_xml, count=1)
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_xml)
    print(f"Added AdMob APPLICATION_ID meta-data to {manifest_path}")
else:
    print(f"AdMob APPLICATION_ID meta-data already present in {manifest_path}, skipping")
