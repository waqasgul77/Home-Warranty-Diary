#!/usr/bin/env python3
"""
Wires the release keystore into android/app/build.gradle using environment
variables, so the signed release AAB build always finds the keystore via a
reliable, absolute path.

Run this after the keystore .jks file has been generated and before
`./gradlew bundleRelease`. The build step must then set these env vars:
  RELEASE_KEYSTORE_PATH, RELEASE_STORE_PASSWORD, RELEASE_KEY_ALIAS, RELEASE_KEY_PASSWORD

It is safe to run more than once — it skips the change if already present.
"""

gradle_path = "android/app/build.gradle"
with open(gradle_path, "r", encoding="utf-8") as f:
    gradle = f.read()

signing_block = """

android.signingConfigs {
    release {
        storeFile file(System.getenv("RELEASE_KEYSTORE_PATH"))
        storePassword System.getenv("RELEASE_STORE_PASSWORD")
        keyAlias System.getenv("RELEASE_KEY_ALIAS")
        keyPassword System.getenv("RELEASE_KEY_PASSWORD")
    }
}
android.buildTypes.release.signingConfig = android.signingConfigs.release
"""

if "RELEASE_KEYSTORE_PATH" not in gradle:
    gradle += signing_block
    with open(gradle_path, "w", encoding="utf-8") as f:
        f.write(gradle)
    print(f"Added release signingConfig to {gradle_path}")
else:
    print(f"Release signingConfig already present in {gradle_path}, skipping")
