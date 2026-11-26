---
title: "Claude Artifacts Desktop Apps: Now on Mac and Windows"
slug: "claude-artifacts-desktop-apps"
date: "2026-11-26T17:42:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["Claude", "Anthropic", "Claude artifacts", "AI tools", "Desktop apps"]
description: "Claude artifacts desktop apps are in beta: install an artifact as a Mac or Windows app with its own icon and window. Plans, permissions and limits explained."
focusKeyword: "claude artifacts desktop apps"
takeaways:
  - "Since November 24, 2026, Claude for Mac and Windows can install an artifact as an app with its own icon and window."
  - "The beta is rolling out on Free, Pro, Max, Ultra, Team and Enterprise plans and needs desktop version 6.28899.0 or later."
  - "Apps start with browser-level access; you can grant app permissions or full access to the computer, and Claude asks again after every update."
  - "Building an app and its requests to Claude count toward plan usage limits, and the apps are not covered by zero data retention."
  - "It does not work on Linux, web or mobile, or for Docs, Slides and Sheets template artifacts."
image: "/images/covers/claude-artifacts-desktop-apps.webp"
imageAlt: "Claude artifacts installed as desktop apps"
format: "md"
---

Anthropic has launched Claude artifacts desktop apps: you can now install an artifact as an app on Mac or Windows. In its [announcement on November 24, 2026](https://claude.com/resources/articles/install-as-app), Anthropic said an installed artifact "gets its own icon and opens in its own window instead of inside Claude." The [Claude help center article](https://support.claude.com/en/articles/18516354-install-an-artifact-as-an-app) says the feature is "rolling out in beta on Free, Pro, Max, Ultra, Team, and Enterprise plans."

For marketers, this means the small tools you already build in Claude, such as a UTM builder, a content calendar or a report viewer, can sit in your dock or Start menu like any other app. When you edit the artifact, the installed app picks up the change.

[TestingCatalog](https://www.testingcatalog.com/anthropic-now-allows-installing-artifacts-as-desktop-apps/) quoted Anthropic engineer Felix Rieseberg saying he has used it to build "terminals, file managers, video editors, comms tools, and even little desktop pets." There are permission settings and limits you should understand before your team installs anything, especially in a company account.

![Claude artifacts desktop apps at a glance: launched November 24, 2026, beta on six plans, Mac and Windows only, desktop version 6.28899.0 or later](/images/infographics/ig-claude-artifacts-desktop-apps-1.webp)

## How Claude artifacts desktop apps work

You need Claude for Mac or Claude for Windows, version 6.28899.0 or later. The help center gives these steps:

1. Open the artifact in the main Claude Desktop window.
2. Open the artifact's title menu, or right-click the artifact.
3. Select "Install as app".
4. Select "Install" to confirm.

"Install as app" is also in the Share menu. On a Mac, installed apps go into a "Claude Apps" folder inside your home Applications folder. On Windows they appear in a "Claude Apps" folder in the Start menu, and you can add a desktop shortcut. You can also open them from File > Apps in Claude Desktop.

To open an app you have to be online and signed in to Claude Desktop. Anthropic says apps use your Claude account, so there is no API key or separate login.

## Permissions: three levels of access

This is the part IT teams will care about. Each app starts at the lowest level, and you choose whether to give it more.

| Level | What the app can do |
|---|---|
| Default | Only what it could do in a browser |
| App permissions | Notifications, keyboard shortcuts, floating over other windows, a menu bar item on macOS or a system tray icon on Windows |
| Full access to this computer | Run programs and read, change or delete files "without asking each time" |

An "Allow" covers one version of the app only. "After any update, including your own edits, Claude asks again." Full access is generally not allowed for apps with parts written outside your organization, or whose author Claude can't confirm. The help center also warns that "Anthropic doesn't review apps before you install them," and an app from outside your organization shows a warning.

Apps that live in the menu bar or system tray keep running after you close their window.

## Plans, admin settings and limits

On Team plans the feature is on by default, but full computer access stays off until an admin enables it. On Enterprise plans the whole feature is off until an owner turns it on in Organization settings > Artifacts.

Some limits are worth knowing before you plan around this:

- "Building an app, and any requests an app makes to Claude, count toward your plan's usage limits."
- "These apps aren't covered by zero data retention."
- It is not available on Linux, the web or mobile.
- Artifacts made from the Docs, Slides and Sheets templates, legacy artifacts and live artifacts from Claude Cowork can't be installed.
- Anthropic's announcement says HIPAA-ready organizations and hybrid deployments are excluded.
- The help center says full access is not available in Claude for Teachers or for K-12 organizations.

On macOS, Claude can see an installed app through computer use but can't click or type in it. To remove an app, go to File > Apps, select it and choose "Uninstall." That removes the permissions you granted but doesn't delete the artifact.

## What marketing teams should do now

![Steps for Claude artifacts desktop apps: update Claude Desktop, pick one tool to install, keep default access, set admin rules, watch usage limits](/images/infographics/ig-claude-artifacts-desktop-apps-2.webp)

These are our recommendations, not Anthropic guidance.

1. Update Claude Desktop to 6.28899.0 or later and check that "Install as app" shows on one of your artifacts.
2. Pick one tool your team opens every day, such as a campaign naming helper or a brief template, and install that first. Our post on [Claude Sheets and Whiteboards](/claude-sheets-whiteboards-data-marketers/) has ideas for data tools worth building.
3. Leave apps at default access unless a tool truly needs files on your computer. Never grant full access to an app someone outside your company built.
4. If you are a Team or Enterprise admin, decide who may enable full access before staff start asking, and write it down.
5. Keep client data out of apps if your contracts need zero data retention, because these apps are not covered by it.
6. Watch usage. An app that calls Claude every few minutes uses the same plan limits as your chats. If you are choosing a model for a heavy app, our [Claude Fable 5.2 guide](/claude-fable-5-2-marketers/) covers Anthropic's latest model.

Anthropic's [usage policy](/anthropic-usage-policy-ai-answer-seeding/) still applies to whatever you build. If you compare AI workspaces, [ChatGPT Space](/chatgpt-space-plus-users/) is OpenAI's take on shared pages and slides.

## FAQ about Claude artifacts desktop apps

### Is installing artifacts as apps free?

It is rolling out in beta on all plans, including Free. Building and running apps counts toward your plan's usage limits.

### Can I use it on Linux or my phone?

No. It works only in Claude for Mac and Claude for Windows.

### Can an installed app delete my files?

Only if you give it "Full access to this computer." By default an app can only do what it could do in a browser.

### Does uninstalling delete the artifact?

No. Uninstalling removes the permissions you allowed and keeps the artifact.
