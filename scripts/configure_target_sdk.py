#!/usr/bin/env python3
"""
Google Play requires apps to target a recent Android API level (it moves up
roughly once a year). This script bumps the generated Capacitor Android
project to target/compile API 36, and bumps the Android Gradle Plugin +
Gradle wrapper to versions that know how to build against API 36.

Run this AFTER `npx cap add android` and BEFORE the gradle build step.
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANDROID = ROOT / "android"

TARGET_API = "36"
AGP_VERSION = "8.7.2"
GRADLE_VERSION = "8.9"


def patch(path, pattern, replacement, label):
    if not path.exists():
        print(f"skip (not found): {path}")
        return
    text = path.read_text()
    new_text, count = re.subn(pattern, replacement, text)
    if count:
        path.write_text(new_text)
        print(f"updated {label} in {path} ({count} change(s))")
    else:
        print(f"WARNING: pattern for {label} not found in {path} — check manually")


# 1) variables.gradle — compileSdkVersion / targetSdkVersion
patch(
    ANDROID / "variables.gradle",
    r"compileSdkVersion\s*=\s*\d+",
    f"compileSdkVersion = {TARGET_API}",
    "compileSdkVersion",
)
patch(
    ANDROID / "variables.gradle",
    r"targetSdkVersion\s*=\s*\d+",
    f"targetSdkVersion = {TARGET_API}",
    "targetSdkVersion",
)

# 2) root build.gradle — Android Gradle Plugin version
patch(
    ANDROID / "build.gradle",
    r"classpath\s+['\"]com\.android\.tools\.build:gradle:[^'\"]+['\"]",
    f"classpath 'com.android.tools.build:gradle:{AGP_VERSION}'",
    "Android Gradle Plugin version",
)

# 3) gradle wrapper — Gradle version (needs to be new enough for the AGP above)
patch(
    ANDROID / "gradle" / "wrapper" / "gradle-wrapper.properties",
    r"distributionUrl=.*",
    f"distributionUrl=https\\://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-all.zip",
    "Gradle wrapper version",
)

print("Target SDK configuration complete.")
