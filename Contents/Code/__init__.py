import os

APPLICATIONS_PREFIX = "/applications/apptv"

NAME = L('Title')
ART  = 'art-default.jpg'
ICON = 'icon-default.png'


def Start():
	Plugin.AddPrefixHandler(APPLICATIONS_PREFIX, ApplicationsMainMenu, NAME, ICON, ART)

	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	MediaContainer.title1 = NAME
	MediaContainer.viewGroup = "List"
	MediaContainer.art = R(ART)
	DirectoryItem.thumb = R(ICON)
	VideoItem.thumb = R(ICON)


def GetBasePath():
	return os.path.expanduser(os.path.expandvars(Prefs['basepath']))


def ValidatePrefs():
	if (os.path.isdir(GetBasePath())):
		return MessageContainer(
			L('Success'),
			L('SettingsUpdated')
		)
	else:
		return MessageContainer(
			L('Error'),
			L('InvalidBasepath')
		)


def ApplicationsMainMenu():
	dir = MediaContainer(viewGroup="InfoList")

	basePath = GetBasePath()
	applications = os.listdir(basePath)

	for application in applications:
		name = os.path.basename(application)

		# Only append non-hidden .apps or extension-less files (presumed aliases)
		if (("." not in name) or (not name.startswith(".") and name.endswith(".app"))):
			name = os.path.splitext(name)[0]

			dir.Append(
				Function(
					DirectoryItem(
						LaunchApplication,
						name,
						subtitle=L('LaunchSubtitle'),
						summary=L('LaunchSummary') + name,
						thumb=R(ICON),
						art=R(ART)
					),
					path = basePath + "/" + application
				)
			)

	dir.Append(
		PrefsItem(
			title=L('PreferencesTitle'),
			subtile=L('PreferencesSubtitle'),
			summary=L('PreferencesSummary'),
			thumb=R(ICON)
		)
	)

	return dir


def LaunchApplication(sender, path):
	os.system("open " + path)
