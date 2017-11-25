#! /usr/local/bin/python3

import eg

eg.RegisterPlugin(
    name = "Samsung TV (IP) 2016+",
    description = "Control 2016/2017 Samsung TVs via IP.  Requires that \
    you've configured your TV to auto allow remote connections",
    author = "RedsGT",
    version = "1.0",
    kind = "external",
    guid = "{DBE93E00-5645-4CC6-BB0E-0A9D41586709}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=TBD", 
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAA"
        "AAd0SU1FB9YDBAsPCqtpoiUAAAAWdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCAyLjZsqHS1"
        "AAADe0lEQVQ4T02TXVCUZRSAPyZsxpnqoovum+miq+6qFUJYQP7cogS2VpGFAAlKpyAC"
        "EVh+4k80WGADQWlxZRfZACH5ECVY5TdHiEbAIQVkHRzUCZK/ZWGXp10SxjPzXrzvvM9z"
        "zpw5xwUQXg7ndX1jw3VkYmrzycK/gusrgrB3z17hvXfffv2tN99YcXHEi///g07Bznkw"
        "+9i1yvAbqvJKolRJhJ2KQp4ZQWTWd5wsV9Ni6sWybn3tZWYXvjt531V1tgJF8lcEZbij"
        "MLgRbTpAVHcgyk5/QnSefHrmc7QdV1hbX9+VbAvuTk67ZpfVIDsWgu/ZfURfD+TElVBy"
        "m4+TooshvDaAL697EPOHLzK1L9prbayuWbYlwsLzFZfCql+Qx8XhqfoAZUsIhsEGLGsW"
        "Nm12FlZtTM0/w2DSEmn0dEgclRSFcFG8wcamTRAqtO0kpRficdQLpV5Gr7mf3qFHzC1u"
        "YF61MvrIztD0OsP3F6m/ZUDZ7klosxfxJZn0j04hpJ+uIvZ4EpJvJKhvFWOzW1lc2qT/"
        "zznuzdnoGnlG+8BDWnvMDE7M8q1eQcygN6GFkWj0nQgp+WUcilTyUaIHzRPtWKx2rLYt"
        "5hfXHBnMNIjDtHbfY3RmmcdLdkrEfKIHDyDLPYS6vhnhh9wSgiPCcYvbT+3gNQbGluib"
        "WOTG8EOaTGOY/nrKwPgynXdm+H3gCZkNeQ6BP0GnZGgMRoTUnDMcSfgaiUJKWuPP6MRx"
        "LhjvUN3Qh671NnVNQ1y9Oe2YgUmaeqY4WnMEpSgl5ORhzhmaEFRFpSTnOpool+GXFoa6"
        "sQNNXReVupucv9zHeWM3Gl0HNY0mci7VEtF2EJ+8fSTkpSP23EaYmpl1ySgowk8ehiTc"
        "i6iiExRcNKC+0IlG20m5XqRCK5J9qYxoMZSgail+scEUn6vn+bJFImxtbQkl5dWoCkvx"
        "Cg3k/Uh3grKCSahJJln3E8n1BSQ2JhArHuSTUgneET6kFWno6h3GyW5P4sqqRUhMLSCn"
        "uJQA+cdIFYF8GC3F/Xs3vDM8kaZ4sP+YD/4RX5B+Wk1l3SXnkG2zu7uwZrHuqa1rILuw"
        "hNSsfOSxsQQoPkN2WI4iPp7EzBx+dPRLb7zK0orl1Z2FEmwvTM4HZ0kzZvM7hqZfMbaJ"
        "jEw8YHh8kvrGFmr1euaf/iPZAW12uzD2t1n4DwtSpLoLWTYZAAAAAElFTkSuQmCC"
    )
)

import wx
import samsungctl
import time
import wakeonlan
from wakeonlan import wol

class Text:
    tcpBox = "Settings"
    nameLabel = "Name:"
    descriptionLabel = 'Description:'
    idLabel = 'ID:'
    hostLabel = "Host:"
    portLabel = "Port:"
    MACLabel = 'MAC Address of TV:'
    timeoutLabel = 'Timeout:'
    
    nameDescription = "Remote access Name sent to TV."
    descriptionDescription = 'Type of remote access device.'
    idDescription = 'Should be able to leave this blank.'
    hostDescription = "IP address of TV."
    portDescription = "Usually 8001 or 55000. Max=65535"
    MACDescription = 'Needed for Power On.  XX:XX:XX:XX:XX:XX'
    timeoutDescription = 'Timeout in Seconds. Max=120'
    
    eventBox = "Event generation"
    useNewEvents = "Use new events"
    
ACTIONS = (
    ("Poweroff","Power off", None, 'KEY_POWER'),
    ("Up","Up", None, 'KEY_UP'),
    ("Down","Down", None, 'KEY_DOWN'),
    ("Left","Left", None, 'KEY_LEFT'),
    ("Right","Right", None, 'KEY_RIGHT'),
    ("ChannelUp","Page Up", None, 'KEY_CHUP'),
    ("ChannelDown","Channel Down", None, 'KEY_CHDOWN'),
    ("Enter","Enter", None, 'KEY_ENTER'),
    ("Return","Return", None, 'KEY_RETURN'),    
    ("ChannelList","Channel List", None, 'KEY_CH_LIST'),
    ("Menu","Menu", None, 'KEY_MENU'),
    ("Source","Source", None, 'KEY_SOURCE'),
    ("Guide","Guide", None, 'KEY_GUIDE'),
    ("Tools","Tools", None, 'KEY_TOOLS'),
    ("Info","Info", None, 'KEY_INFO'),
    ("red","A / Red", None, 'KEY_RED'),
    ("green","B / Green", None, 'KEY_GREEN'),
    ("yellow","C / Yellow", None, 'KEY_YELLOW'),
    ("blue","D / Blue", None, 'KEY_BLUE'    ),
    ("3D","3D", None, 'KEY_PANNEL_CHDOWN'),
    ("VolumeUp","Volume Up", None, 'KEY_VOLUP'),
    ("VolumeDown","Volume Down", None, 'KEY_VOLDOWN'),    
    ("Mute","Mute", None, 'KEY_MUTE'),    
    ("Num0","Num 0", None, 'KEY_0'),
    ("Num1","Num 1", None, 'KEY_1'),
    ("Num2","Num 2", None, 'KEY_2'),
    ("Num3","Num 3", None, 'KEY_3'),
    ("Num4","Num 4", None, 'KEY_4'),
    ("Num5","Num 5", None, 'KEY_5'),
    ("Num6","Num 6", None, 'KEY_6'),
    ("Num7","Num 7", None, 'KEY_7'),
    ("Num8","Num 8", None, 'KEY_8'),
    ("Num9","Num 9", None, 'KEY_9'),
    ("TVSource","TV Source", None, 'KEY_DTV'),
    ("HDMISource","HDMI Source", None, 'KEY_HDMI')
    )

ACTIONSUPDATE = (
    ('fnKEY_1', 'Key1', None, 'KEY_1'), 
    ('fnKEY_2', 'Key2', None, 'KEY_2'), 
    ('fnKEY_3', 'Key3', None, 'KEY_3'), 
    ('fnKEY_4', 'Key4', None, 'KEY_4'), 
    ('fnKEY_5', 'Key5', None, 'KEY_5'), 
    ('fnKEY_6', 'Key6', None, 'KEY_6'), 
    ('fnKEY_7', 'Key7', None, 'KEY_7'), 
    ('fnKEY_8', 'Key8', None, 'KEY_8'), 
    ('fnKEY_9', 'Key9', None, 'KEY_9'), 
    ('fnKEY_0', 'Key0', None, 'KEY_0'), 
    ('fnKEY_CHUP', 'ChannelUp', None, 'KEY_CHUP'), 
    ('fnKEY_CHDOWN', 'ChannelDown', None, 'KEY_CHDOWN'), 
    ('fnKEY_VOLUP', 'VolUp', None, 'KEY_VOLUP'),
    ('fnKEY_VOLDOWN', 'VolDown', None, 'KEY_VOLDOWN'), 
    ('fnKEY_MENU', 'Menu', None, 'KEY_MENU'), 
    ('fnKEY_UP', 'Up', None, 'KEY_UP'), 
    ('fnKEY_DOWN', 'Down', None, 'KEY_DOWN'), 
    ('fnKEY_LEFT', 'Left', None, 'KEY_LEFT'), 
    ('fnKEY_RIGHT', 'Right', None, 'KEY_RIGHT'), 
    ('fnKEY_MUTE', 'Mute', None, 'KEY_MUTE'),
    ('fnKEY_PRECH', 'Pre-Ch', None, 'KEY_PRECH'),
    ('fnKEY_GREEN', 'Green', None, 'KEY_GREEN'),
    ('fnKEY_YELLOW', 'Yellow', None, 'KEY_YELLOW'),
    ('fnKEY_CYAN', 'Cyan', None, 'KEY_CYAN'),
    ('fnKEY_ADDDEL', 'Add/Del', None, 'KEY_ADDDEL'),
    ('fnKEY_SOURCE', 'Source', None, 'KEY_SOURCE'),
    ('fnKEY_INFO', 'Info', None, 'KEY_INFO'),
    ('fnKEY_PIP_ONOFF', 'PIP', None, 'KEY_PIP_ONOFF'),
    ('fnKEY_PIP_SWAP', 'PIPSwap', None, 'KEY_PIP_SWAP'),
    ('fnKEY_PLUS100', 'Plus100', None, 'KEY_PLUS100'),
    ('fnKEY_CAPTION', 'Ad/Subt.', None, 'KEY_CAPTION'),
    ('fnKEY_PMODE', 'PictureMode', None, 'KEY_PMODE'),
    ('fnKEY_TTX_MIX', 'Teletext', None, 'KEY_TTX_MIX'),
    ('fnKEY_TV', 'TV', None, 'KEY_TV'),
    ('fnKEY_PICTURE_SIZE', 'PictureFormat', None, 'KEY_PICTURE_SIZE'),
    ('fnKEY_AD', 'AD/Subt.', None, 'KEY_AD'),
    ('fnKEY_PIP_SIZE', 'PIPSize', None, 'KEY_PIP_SIZE'),
    ('fnKEY_PIP_CHUP', 'PIPChannelUp', None, 'KEY_PIP_CHUP'),
    ('fnKEY_PIP_CHDOWN', 'PIPChannelDown', None, 'KEY_PIP_CHDOWN'),
    ('fnKEY_ANTENA', 'AntenaTV', None, 'KEY_ANTENA'),
    ('fnKEY_AUTO_PROGRAM', 'AutoProgram', None, 'KEY_AUTO_PROGRAM'),
    ('fnKEY_ASPECT', 'PictureFormat', None, 'KEY_ASPECT'),
    ('fnKEY_TOPMENU', 'Support', None, 'KEY_TOPMENU'),
    ('fnKEY_DTV', 'DigitalTV', None, 'KEY_DTV'),
    ('fnKEY_FAVCH', 'Favorites', None, 'KEY_FAVCH'),
    ('fnKEY_REWIND', 'Rewind', None, 'KEY_REWIND'),
    ('fnKEY_STOP', 'Stop', None, 'KEY_STOP'),
    ('fnKEY_PLAY', 'Play', None, 'KEY_PLAY'),
    ('fnKEY_FF', 'FastForward', None, 'KEY_FF'),
    ('fnKEY_REC', 'Record', None, 'KEY_REC'),
    ('fnKEY_PAUSE', 'Pause', None, 'KEY_PAUSE'),
    ('fnKEY_TOOLS', 'Tools', None, 'KEY_TOOLS'),
    ('fnKEY_LINK', 'Link', None, 'KEY_LINK'),
    ('fnKEY_SLEEP', 'SleepTimer', None, 'KEY_SLEEP'),
    ('fnKEY_TURBO', 'SocialTV', None, 'KEY_TURBO'),
    ('fnKEY_CH_LIST', 'ChannelList', None, 'KEY_CH_LIST'),
    ('fnKEY_RED', 'Red', None, 'KEY_RED'),
    ('fnKEY_HOME', 'Home', None, 'KEY_HOME'),
    ('fnKEY_ESAVING', 'EnergySaving', None, 'KEY_ESAVING'),
    ('fnKEY_CONTENTS', 'SmartTV', None, 'KEY_CONTENTS'),
    ('fnKEY_VCR_MODE', 'VCRmode', None, 'KEY_VCR_MODE'),
    ('fnKEY_CATV_MODE', 'CATVmode', None, 'KEY_CATV_MODE'),
    ('fnKEY_DSS_MODE', 'DSSmode', None, 'KEY_DSS_MODE'),
    ('fnKEY_TV_MODE', 'TVmode', None, 'KEY_TV_MODE'),
    ('fnKEY_DVD_MODE', 'DVDmode', None, 'KEY_DVD_MODE'),
    ('fnKEY_STB_MODE', 'STBmode', None, 'KEY_STB_MODE'),
    ('fnKEY_ZOOM_MOVE', 'KEY_ZOOM_MOVE', None, 'KEY_ZOOM_MOVE'),
    ('fnKEY_CLOCK_DISPLAY', 'ClockDisplay', None, 'KEY_CLOCK_DISPLAY'),
    ('fnKEY_AV1', 'Ext.', None, 'KEY_AV1'),
    ('fnKEY_COMPONENT1', 'Component', None, 'KEY_COMPONENT1'),
    ('fnKEY_SETUP_CLOCK_TIMER', 'SetupClock', None, 'KEY_SETUP_CLOCK_TIMER'),
    ('fnKEY_RETURN', 'Return', None, 'KEY_RETURN'),
    ('fnKEY_HDMI', 'HDMI', None, 'KEY_HDMI'),
    ('fnKEY_POWEROFF', 'PowerOFF', None, 'KEY_POWEROFF'),
    ('fnKEY_PANNEL_CHDOWN', '3D', None, 'KEY_PANNEL_CHDOWN'),
    ('fnKEY_AUTO_ARC_PIP_SMALL', 'PictureModeDynamic', None, 'KEY_AUTO_ARC_PIP_SMALL'),
    ('fnKEY_AUTO_ARC_PIP_WIDE', 'HDMI2', None, 'KEY_AUTO_ARC_PIP_WIDE'),
    ('fnKEY_AUTO_ARC_PIP_RIGHT_BOTTOM', 'HDMI3', None, 'KEY_AUTO_ARC_PIP_RIGHT_BOTTOM'),
    ('fnKEY_AUTO_ARC_PIP_SOURCE_CHANGE', 'BluetoohPair', None, 'KEY_AUTO_ARC_PIP_SOURCE_CHANGE'),
    ('fnKEY_EXT9', 'PictureModeMovie', None, 'KEY_EXT9'),
    ('fnKEY_EXT10', 'PictureModeStandard', None, 'KEY_EXT10'),
    ('fnKEY_EXT14', 'PictureSize_3:4', None, 'KEY_EXT14'),
    ('fnKEY_EXT15', 'PictureSize_16:9', None, 'KEY_EXT15'),
    ('fnKEY_EXT20', 'HDMI1', None, 'KEY_EXT20'),
    ('fnKEY_EXT23', 'AV', None, 'KEY_EXT23'),
    ('fnKEY_AUTO_ARC_C_FORCE_AGING', 'Fam.Story', None, 'KEY_AUTO_ARC_C_FORCE_AGING'),
    ('fnKEY_AUTO_ARC_CAPTION_ENG', 'History', None, 'KEY_AUTO_ARC_CAPTION_ENG'),
    ('fnKEY_AUTO_ARC_USBJACK_INSPECT', 'Camera', None, 'KEY_AUTO_ARC_USBJACK_INSPECT'),
    ('fnKEY_DTV_SIGNAL', 'Search', None, 'KEY_DTV_SIGNAL'),
    ('fnKEY_AV2', 'AllSharePlay', None, 'KEY_AV2'),
    ('fnKEY_CONVERGENCE', 'InternetBrowser', None, 'KEY_CONVERGENCE'),
    ('fnKEY_MAGIC_CHANNEL', 'KEY_MAGIC_CHANNEL', None, 'KEY_MAGIC_CHANNEL'),
    ('fnKEY_PIP_SCAN', 'KEY_PIP_SCAN', None, 'KEY_PIP_SCAN'),
    ('fnKEY_DEVICE_CONNECT', 'KEY_DEVICE_CONNECT', None, 'KEY_DEVICE_CONNECT'),
    ('fnKEY_HELP', 'KEY_HELP', None, 'KEY_HELP'),
    ('fnKEY_11', 'KEY_11', None, 'KEY_11'),
    ('fnKEY_12', 'KEY_12', None, 'KEY_12'),
    ('fnKEY_FACTORY', 'KEY_FACTORY', None, 'KEY_FACTORY'),
    ('fnKEY_3SPEED', 'KEY_3SPEED', None, 'KEY_3SPEED'),
    ('fnKEY_RSURF', 'KEY_RSURF', None, 'KEY_RSURF'),
    ('fnKEY_GAME', 'KEY_GAME', None, 'KEY_GAME'),
    ('fnKEY_QUICK_REPLAY', 'KEY_QUICK_REPLAY', None, 'KEY_QUICK_REPLAY'),
    ('fnKEY_STILL_PICTURE', 'KEY_STILL_PICTURE', None, 'KEY_STILL_PICTURE'),
    ('fnKEY_INSTANT_REPLAY', 'KEY_INSTANT_REPLAY', None, 'KEY_INSTANT_REPLAY'),
    ('fnKEY_FF_', 'KEY_FF_', None, 'KEY_FF_'),
    ('fnKEY_GUIDE', 'KEY_GUIDE', None, 'KEY_GUIDE'),
    ('fnKEY_REWIND_', 'KEY_REWIND_', None, 'KEY_REWIND_'),
    ('fnKEY_ANGLE', 'KEY_ANGLE', None, 'KEY_ANGLE'),
    ('fnKEY_RESERVED1', 'KEY_RESERVED1', None, 'KEY_RESERVED1'),
    ('fnKEY_ZOOM1', 'KEY_ZOOM1', None, 'KEY_ZOOM1'),
    ('fnKEY_PROGRAM', 'KEY_PROGRAM', None, 'KEY_PROGRAM'),
    ('fnKEY_BOOKMARK', 'KEY_BOOKMARK', None, 'KEY_BOOKMARK'),
    ('fnKEY_DISC_MENU', 'KEY_DISC_MENU', None, 'KEY_DISC_MENU'),
    ('fnKEY_PRINT', 'KEY_PRINT', None, 'KEY_PRINT'),
    ('fnKEY_SUB_TITLE', 'KEY_SUB_TITLE', None, 'KEY_SUB_TITLE'),
    ('fnKEY_CLEAR', 'KEY_CLEAR', None, 'KEY_CLEAR'),
    ('fnKEY_VCHIP', 'KEY_VCHIP', None, 'KEY_VCHIP'),
    ('fnKEY_REPEAT', 'KEY_REPEAT', None, 'KEY_REPEAT'),
    ('fnKEY_DOOR', 'KEY_DOOR', None, 'KEY_DOOR'),
    ('fnKEY_OPEN', 'KEY_OPEN', None, 'KEY_OPEN'),
    ('fnKEY_WHEEL_LEFT', 'KEY_WHEEL_LEFT', None, 'KEY_WHEEL_LEFT'),
    ('fnKEY_POWER', 'KEY_POWER', None, 'KEY_POWER'),
    ('fnKEY_DMA', 'KEY_DMA', None, 'KEY_DMA'),
    ('fnKEY_FM_RADIO', 'KEY_FM_RADIO', None, 'KEY_FM_RADIO'),
    ('fnKEY_DVR_MENU', 'KEY_DVR_MENU', None, 'KEY_DVR_MENU'),
    ('fnKEY_MTS', 'KEY_MTS', None, 'KEY_MTS'),
    ('fnKEY_PCMODE', 'KEY_PCMODE', None, 'KEY_PCMODE'),
    ('fnKEY_TTX_SUBFACE', 'KEY_TTX_SUBFACE', None, 'KEY_TTX_SUBFACE'),
    ('fnKEY_DNIe', 'KEY_DNIe', None, 'KEY_DNIe'),
    ('fnKEY_SRS', 'KEY_SRS', None, 'KEY_SRS'),
    ('fnKEY_CONVERT_AUDIO_MAINSUB', 'KEY_CONVERT_AUDIO_MAINSUB', None, 'KEY_CONVERT_AUDIO_MAINSUB'),
    ('fnKEY_MDC', 'KEY_MDC', None, 'KEY_MDC'),
    ('fnKEY_SEFFECT', 'KEY_SEFFECT', None, 'KEY_SEFFECT'),
    ('fnKEY_DVR', 'KEY_DVR', None, 'KEY_DVR'),
    ('fnKEY_LIVE', 'KEY_LIVE', None, 'KEY_LIVE'),
    ('fnKEY_PERPECT_FOCUS', 'KEY_PERPECT_FOCUS', None, 'KEY_PERPECT_FOCUS'),
    ('fnKEY_WHEEL_RIGHT', 'KEY_WHEEL_RIGHT', None, 'KEY_WHEEL_RIGHT'),
    ('fnKEY_SVIDEO1', 'KEY_SVIDEO1', None, 'KEY_SVIDEO1'),
    ('fnKEY_CALLER_ID', 'KEY_CALLER_ID', None, 'KEY_CALLER_ID'),
    ('fnKEY_SCALE', 'KEY_SCALE', None, 'KEY_SCALE'),
    ('fnKEY_COMPONENT2', 'KEY_COMPONENT2', None, 'KEY_COMPONENT2'),
    ('fnKEY_MAGIC_BRIGHT', 'KEY_MAGIC_BRIGHT', None, 'KEY_MAGIC_BRIGHT'),
    ('fnKEY_DVI', 'KEY_DVI', None, 'KEY_DVI'),
    ('fnKEY_W_LINK', 'KEY_W_LINK', None, 'KEY_W_LINK'),
    ('fnKEY_DTV_LINK', 'KEY_DTV_LINK', None, 'KEY_DTV_LINK'),
    ('fnKEY_APP_LIST', 'KEY_APP_LIST', None, 'KEY_APP_LIST'),
    ('fnKEY_BACK_MHP', 'KEY_BACK_MHP', None, 'KEY_BACK_MHP'),
    ('fnKEY_ALT_MHP', 'KEY_ALT_MHP', None, 'KEY_ALT_MHP'),
    ('fnKEY_DNSe', 'KEY_DNSe', None, 'KEY_DNSe'),
    ('fnKEY_RSS', 'KEY_RSS', None, 'KEY_RSS'),
    ('fnKEY_ENTERTAINMENT', 'KEY_ENTERTAINMENT', None, 'KEY_ENTERTAINMENT'),
    ('fnKEY_ID_INPUT', 'KEY_ID_INPUT', None, 'KEY_ID_INPUT'),
    ('fnKEY_ID_SETUP', 'KEY_ID_SETUP', None, 'KEY_ID_SETUP'),
    ('fnKEY_ANYNET', 'KEY_ANYNET', None, 'KEY_ANYNET'),
    ('fnKEY_POWERON', 'KEY_POWERON', None, 'KEY_POWERON'),
    ('fnKEY_ANYVIEW', 'KEY_ANYVIEW', None, 'KEY_ANYVIEW'),
    ('fnKEY_MS', 'KEY_MS', None, 'KEY_MS'),
    ('fnKEY_MORE', 'KEY_MORE', None, 'KEY_MORE'),
    ('fnKEY_PANNEL_POWER', 'KEY_PANNEL_POWER', None, 'KEY_PANNEL_POWER'),
    ('fnKEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP', None, 'KEY_PANNEL_CHUP'),
    ('fnKEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP', None, 'KEY_PANNEL_VOLUP'),
    ('fnKEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW', None, 'KEY_PANNEL_VOLDOW'),
    ('fnKEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', None, 'KEY_PANNEL_ENTER'),
    ('fnKEY_PANNEL_MENU', 'KEY_PANNEL_MENU', None, 'KEY_PANNEL_MENU'),
    ('fnKEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE', None, 'KEY_PANNEL_SOURCE'),
    ('fnKEY_AV3', 'KEY_AV3', None, 'KEY_AV3'),
    ('fnKEY_SVIDEO2', 'KEY_SVIDEO2', None, 'KEY_SVIDEO2'),
    ('fnKEY_SVIDEO3', 'KEY_SVIDEO3', None, 'KEY_SVIDEO3'),
    ('fnKEY_ZOOM2', 'KEY_ZOOM2', None, 'KEY_ZOOM2'),
    ('fnKEY_PANORAMA', 'KEY_PANORAMA', None, 'KEY_PANORAMA'),
    ('fnKEY_4_3', 'KEY_4_3', None, 'KEY_4_3'),
    ('fnKEY_16_9', 'KEY_16_9', None, 'KEY_16_9'),
    ('fnKEY_DYNAMIC', 'KEY_DYNAMIC', None, 'KEY_DYNAMIC'),
    ('fnKEY_STANDARD', 'KEY_STANDARD', None, 'KEY_STANDARD'),
    ('fnKEY_MOVIE1', 'KEY_MOVIE1', None, 'KEY_MOVIE1'),
    ('fnKEY_CUSTOM', 'KEY_CUSTOM', None, 'KEY_CUSTOM'),
    ('fnKEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET', None, 'KEY_AUTO_ARC_RESET'),
    ('fnKEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON', None, 'KEY_AUTO_ARC_LNA_ON'),
    ('fnKEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF', None, 'KEY_AUTO_ARC_LNA_OFF'),
    ('fnKEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK', None, 'KEY_AUTO_ARC_ANYNET_MODE_OK'),
    ('fnKEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START', None, 'KEY_AUTO_ARC_ANYNET_AUTO_START'),
    ('fnKEY_AUTO_FORMAT', 'KEY_AUTO_FORMAT', None, 'KEY_AUTO_FORMAT'),
    ('fnKEY_DNET', 'KEY_DNET', None, 'KEY_DNET'),
    ('fnKEY_HDMI1', 'KEY_HDMI1', None, 'KEY_HDMI1'),
    ('fnKEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON', None, 'KEY_AUTO_ARC_CAPTION_ON'),
    ('fnKEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF', None, 'KEY_AUTO_ARC_CAPTION_OFF'),
    ('fnKEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE', None, 'KEY_AUTO_ARC_PIP_DOUBLE'),
    ('fnKEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE', None, 'KEY_AUTO_ARC_PIP_LARGE'),
    ('fnKEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP', None, 'KEY_AUTO_ARC_PIP_LEFT_TOP'),
    ('fnKEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP', None, 'KEY_AUTO_ARC_PIP_RIGHT_TOP'),
    ('fnKEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM', None, 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM'),
    ('fnKEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE', None, 'KEY_AUTO_ARC_PIP_CH_CHANGE'),
    ('fnKEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS', None, 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS'),
    ('fnKEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL', None, 'KEY_AUTO_ARC_AUTOCOLOR_FAIL'),
    ('fnKEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT', None, 'KEY_AUTO_ARC_JACK_IDENT'),
    ('fnKEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE', None, 'KEY_NINE_SEPERATE'),
    ('fnKEY_ZOOM_IN', 'KEY_ZOOM_IN', None, 'KEY_ZOOM_IN'),
    ('fnKEY_ZOOM_OUT', 'KEY_ZOOM_OUT', None, 'KEY_ZOOM_OUT'),
    ('fnKEY_MIC', 'KEY_MIC', None, 'KEY_MIC'),
    ('fnKEY_HDMI2', 'KEY_HDMI2', None, 'KEY_HDMI2'),
    ('fnKEY_HDMI3', 'KEY_HDMI3', None, 'KEY_HDMI3'),
    ('fnKEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR', None, 'KEY_AUTO_ARC_CAPTION_KOR'),
    ('fnKEY_HDMI4', 'KEY_HDMI4', None, 'KEY_HDMI4'),
    ('fnKEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR', None, 'KEY_AUTO_ARC_ANTENNA_AIR'),
    ('fnKEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE', None, 'KEY_AUTO_ARC_ANTENNA_CABLE'),
    ('fnKEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE', None, 'KEY_AUTO_ARC_ANTENNA_SATELLITE'),
    ('fnKEY_EXT1', 'KEY_EXT1', None, 'KEY_EXT1'),
    ('fnKEY_EXT2', 'KEY_EXT2', None, 'KEY_EXT2'),
    ('fnKEY_EXT3', 'KEY_EXT3', None, 'KEY_EXT3'),
    ('fnKEY_EXT4', 'KEY_EXT4', None, 'KEY_EXT4'),
    ('fnKEY_EXT5', 'KEY_EXT5', None, 'KEY_EXT5'),
    ('fnKEY_EXT6', 'KEY_EXT6', None, 'KEY_EXT6'),
    ('fnKEY_EXT7', 'KEY_EXT7', None, 'KEY_EXT7'),
    ('fnKEY_EXT8', 'KEY_EXT8', None, 'KEY_EXT8'),
    ('fnKEY_EXT11', 'KEY_EXT11', None, 'KEY_EXT11'),
    ('fnKEY_EXT12', 'KEY_EXT12', None, 'KEY_EXT12'),
    ('fnKEY_EXT13', 'KEY_EXT13', None, 'KEY_EXT13'),
    ('fnKEY_EXT16', 'KEY_EXT16', None, 'KEY_EXT16'),
    ('fnKEY_EXT17', 'KEY_EXT17', None, 'KEY_EXT17'),
    ('fnKEY_EXT18', 'KEY_EXT18', None, 'KEY_EXT18'),
    ('fnKEY_EXT19', 'KEY_EXT19', None, 'KEY_EXT19'),
    ('fnKEY_EXT21', 'KEY_EXT21', None, 'KEY_EXT21'),
    ('fnKEY_EXT22', 'KEY_EXT22', None, 'KEY_EXT22'),
    ('fnKEY_EXT24', 'KEY_EXT24', None, 'KEY_EXT24'),
    ('fnKEY_EXT25', 'KEY_EXT25', None, 'KEY_EXT25'),
    ('fnKEY_EXT26', 'KEY_EXT26', None, 'KEY_EXT26'),
    ('fnKEY_EXT27', 'KEY_EXT27', None, 'KEY_EXT27'),
    ('fnKEY_EXT28', 'KEY_EXT28', None, 'KEY_EXT28'),
    ('fnKEY_EXT29', 'KEY_EXT29', None, 'KEY_EXT29'),
    ('fnKEY_EXT30', 'KEY_EXT30', None, 'KEY_EXT30'),
    ('fnKEY_EXT31', 'KEY_EXT31', None, 'KEY_EXT31'),
    ('fnKEY_EXT32', 'KEY_EXT32', None, 'KEY_EXT32'),
    ('fnKEY_EXT33', 'KEY_EXT33', None, 'KEY_EXT33'),
    ('fnKEY_EXT34', 'KEY_EXT34', None, 'KEY_EXT34'),
    ('fnKEY_EXT35', 'KEY_EXT35', None, 'KEY_EXT35'),
    ('fnKEY_EXT36', 'KEY_EXT36', None, 'KEY_EXT36'),
    ('fnKEY_EXT37', 'KEY_EXT37', None, 'KEY_EXT37'),
    ('fnKEY_EXT38', 'KEY_EXT38', None, 'KEY_EXT38'),
    ('fnKEY_EXT39', 'KEY_EXT39', None, 'KEY_EXT39'),
    ('fnKEY_EXT40', 'KEY_EXT40', None, 'KEY_EXT40'),
    ('fnKEY_EXT41', 'KEY_EXT41', None, 'KEY_EXT41')
    )

class SamsungIP(eg.PluginBase):
    
    def __init__(self):
        #self.name = 'eventghost'
        #self.description = 'PC'
        #self.idid = ''
        #self.host="192.168.1.x"
        #self.port=8001
        #self.mac = ''
        #self.timeout = '5'
        self.AddActionsFromList(ACTIONSUPDATE, SendCommandTemplate)
        self.AddAction(TurnOn)
        self.AddAction(AKey)
        
    def __start__(
        self,
        name = 'eventghost',
        description = 'PC',
        idid = '',
        host="192.168.1.x",
        port=8001,
        mac = '',
        timeout = 5,
        dummy1=None,
        dummy2=None,
        useNewEvents=True
    ):
        self.name = name
        self.description = description
        self.idid = idid
        self.host=host
        self.port=port
        self.mac = mac
        self.timeout = timeout
        
        #print "Debug output:"
        #print self.name
        #print self.description
        #print self.idid
        #print self.host
        #print self.mac
        #print self.timeout
    
    text = Text
    def Configure(
        self,
        name = 'eventghost',
        description = 'PC',
        idid = '',
        host="192.168.1.x",
        port=8001,
        mac = '',
        timeout = 5,
        dummy1=None,
        dummy2=None,
        useNewEvents=True
    ):
        text = self.text
        panel = eg.ConfigPanel()
        nameCtrl = panel.TextCtrl(name)
        descriptionCtrl = panel.TextCtrl(description)
        idCtrl = panel.TextCtrl(idid)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        MACCtrl = panel.TextCtrl(mac)
        timeoutCtrl = panel.SpinIntCtrl(timeout, max=120)
        newEventCtrl = panel.CheckBox(useNewEvents, text.useNewEvents)

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.nameLabel, nameCtrl, text.nameDescription),
            (text.descriptionLabel, descriptionCtrl, text.descriptionDescription),
            (text.idLabel, idCtrl, text.idDescription),
            (text.hostLabel, hostCtrl, text.hostDescription),
            (text.portLabel, portCtrl, text.portDescription),
            (text.MACLabel, MACCtrl, text.MACDescription),
            (text.timeoutLabel, timeoutCtrl, text.timeoutDescription)
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        eg.EqualizeWidths(tcpBox.GetColumnItems(1))
        eventBox = panel.BoxedGroup(
            text.eventBox,
            newEventCtrl,
        )
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                descriptionCtrl.GetValue(),
                idCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                MACCtrl.GetValue(),
                timeoutCtrl.GetValue(),
                None,
                None,
                newEventCtrl.GetValue(),
            )
            


class SendCommandTemplate(eg.ActionClass):

    def __call__(self):
        
        #print "Debug SendCommand output:"
        #print self.plugin.name
        #print self.plugin.description
        #print self.plugin.idid
        #print self.plugin.host
        #print self.plugin.mac
        #print self.plugin.timeout
        
        config = {
            "name": self.plugin.name,
            "description": self.plugin.description,
            "id": self.plugin.idid,
            "host": self.plugin.host,
            "port": self.plugin.port,
            "method": "websocket",
            "timeout": "5"
        }
        with samsungctl.Remote(config) as remote:
            remote.control(self.value)

class TurnOn(eg.ActionBase):
    def __call__(self):
        wol.send_magic_packet(self.plugin.mac)
        #wol.send_magic_packet('54:bd:79:95:19:ef')

class AKey(eg.ActionWithStringParameter):
    def __call__(self,cmd):
        self.name = "Custom Key"
        config = {
            "name": self.plugin.name,
            "description": self.plugin.description,
            "id": self.plugin.idid,
            "host": self.plugin.host,
            "port": self.plugin.port,
            "method": "websocket",
            "timeout": "5"
        }
        with samsungctl.Remote(config) as remote:
            remote.control(cmd)
