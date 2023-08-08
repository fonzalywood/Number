import utils as u
import re
#from tools import *
import sys
from exportTelegraph import *
import asyncio
# Push from terminal from a second user
# git config --local credential.helper ""


def main():
    asyncio.run(export_messages())
    

async def export_messages():
    
        channel_dict = dict()  # {channel_id: channel_name}
        
        try:
            events = exportEvents()
            cleansed_content = cleanse_events(events)
            
            extras = exportExtras()
            cleansed_content += cleanse_elcano(extras)

            misCanales = exportMisCanales()
            cleansed_content += cleanse_misCanales(misCanales)
            
            elcano = read_cached_elcano()
            cleansed_content += cleanse_elcano(elcano)
            
            channel_dict = update_channel_dict(cleansed_content, channel_dict)
    
        except Exception as e:
            print("exportMessages : ERROR :", e)
            sys.exit(1)
            
        export_channels(channel_dict)

'''
def read_cached_events():
    with open('caches/eventos telegraph.txt', 'r') as cachedlist:
        contenido = cachedlist.read()
        cachedlist.close()
        print("read_cached_events: INFO: returning eventos cacheados")
        return (contenido)


def read_cached_extras():
    with open('caches/extras telegraph.txt', 'r') as cachedlist:
        contenido = cachedlist.read()
        cachedlist.close()
        print("read_cached_extras: INFO: returning extras cacheados")
        return (contenido)
'''

def read_cached_elcano():
    with open('caches/cachedList.txt', 'r') as cachedlist:
        contenido = cachedlist.read()
        cachedlist.close()
        print("read_cached_elcano: INFO: returning elcano cacheado")
        return (contenido)


def cleanse_events(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'

    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row):
                if i > 0:
                    cleansed_content += "_" + rows[i - 1] + "\n" + row + "\n"
                else:
                    cleansed_content += "_" + "UNTITLED CHANNEL" + "\n" + row + "\n"

    return cleansed_content

def cleanse_misCanales(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'

    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row):
                if i > 0:
                    cleansed_content += "*" + rows[i - 1] + "\n" + row + "\n"
                else:
                    cleansed_content += "*" + "UNTITLED CHANNEL" + "\n" + row + "\n"

    return cleansed_content
  
def cleanse_elcano(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'
    
    if re.search(channel_id_regex, message_content):
        for i, row in enumerate(rows):
            if re.search(channel_id_regex, row):
                if i > 0:
                  cleansed_content += rows[i-1] + "\n" + row + "\n"
                else:
                  cleansed_content += "UNTITLED CHANNEL" + "\n" + row + "\n"

    return cleansed_content


def update_channel_dict(message_content, channel_dict):
    
    rows = message_content.split("\n")
    
    for i, row in enumerate(rows):
        if i % 2 == 1:
            channel_id = row
            channel_name = rows[i-1]
            channel_name = u.correct_channel_name(channel_name)    
            channel_dict[channel_id] = channel_name
    
    return channel_dict


def export_channels(channel_dict):
    
    channel_list = []
    #print(channel_dict)
    for channel_id, channel_name in channel_dict.items():
        group_title = u.extract_group_title(channel_name)
        tvg_id = u.extract_tvg_id(channel_name)
        logo = u.get_logo(tvg_id)
        identif = (channel_id[0:4])
        if channel_name.startswith("_"):
            channel_name = channel_name[1:]
        if channel_name.startswith("*"):
            channel_name = channel_name[1:]
        channel_info = {"group_title": group_title,
                        "tvg_id": tvg_id,
                        "logo": logo,
                        "channel_id": channel_id,
                        "channel_name": channel_name + "  " + identif}
        #print(channel_info)
        channel_list.append(channel_info)

    # CANALES AÑADIDOS QUE ENTRAN EN LA LÓGICA DEL SCRIPT
    channel_list.append({'group_title': 'DAZN F1', 'tvg_id': '','logo': 'https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/012018/untitled-1_20.png?An9Fa1zRO4z6Dj__EVR4da6YOWsvtEw2&itok=6PiLMTa5', 'channel_id': 'https://www.f1-tempo.com/', 'channel_name': 'F1 Tempo Telemetría'})
    #channel_list.append({'group_title': 'DAZN F1', 'tvg_id': 'DAZN F1 HD','logo': 'https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/012018/untitled-1_20.png?An9Fa1zRO4z6Dj__EVR4da6YOWsvtEw2&itok=6PiLMTa5', 'channel_id': 'ACESTREAM ID', 'channel_name': 'F1 Multicámara by Álex'})
    channel_list.append({'group_title': 'electroperra', 'tvg_id': 'HISTORIA', 'logo': 'https://www.movistarplus.es/recorte/m-NEO/canal/HIST.png', 'channel_id': 'http://mol-2.com:8080/play/live.php?mac=00:1A:79:C3:AF:36&stream=55609&extension=ts&play_token=ltn2GgE1z6', 'channel_name': 'Historia'})
    channel_list.append({'group_title': 'electroperra', 'tvg_id': 'NAT GEO WILD HD', 'logo': 'https://www.movistarplus.es/recorte/m-NEO/canal/NATGW.png', 'channel_id': 'http://mol-2.com:8080/play/live.php?mac=00:1A:79:C3:AF:36&stream=55611&extension=ts&play_token=ltn2GgE1z6', 'channel_name': 'Nat Geo Wild'})
    channel_list.append({'group_title': 'electroperra', 'tvg_id': 'NAT GEO HD', 'logo': 'https://www.movistarplus.es/recorte/m-NEO/canal/NATGEO.png', 'channel_id': 'http://mol-2.com:8080/play/live.php?mac=00:1A:79:C3:AF:36&stream=55613&extension=ts&play_token=ltn2GgE1z6', 'channel_name': 'National Geographic'})

    all_channels = ""
    all_channels += '#EXTM3U url-tvg="https://raw.githubusercontent.com/davidmuma/EPG_dobleM/master/guia.xml, https://raw.githubusercontent.com/acidjesuz/EPG/master/guide.xml"\n'

    # CANALES AÑADIDOS AL PRINCIPIO DE LA LISTA
    #all_channels += '#EXTINF:-1 tvg-logo="https://logodownload.org/wp-content/uploads/2017/11/telegram-logo-0-2.png" ,HACKS LOVE + ROBOTS\nhttps://t.me/+__T5lqenMkcwMzdk\n'
    #all_channels += '#EXTINF:-1 tvg-logo="https://telegra.ph/file/fba058a81f4038f75c076.jpg" ,Wimbledon 4K UHD by Álex\nacestream://3470a98b59416289f0e6d206b6979a0dc26defa8\n'
    #all_channels += '#EXTINF:-1 tvg-logo="https://telegra.ph/file/fba058a81f4038f75c076.jpg" ,Wimbledon UHD by Ronki\nacestream://78aa81aedb1e2b6a9ba178398148940857155f6a\n'
    #all_channels += '#EXTINF:-1 tvg-id="I401.1229.tvguide.co.uk" tvg-logo="https://telegra.ph/file/fba058a81f4038f75c076.jpg" ,Sky Sports Main Event\nacestream://eab7aeef0218ce8b0752e596e4792b69eda4df5e\n'
    #all_channels += '#EXTINF:-1 tvg-logo="https://telegra.ph/file/fba058a81f4038f75c076.jpg" ,Sky Sports Arena\nacestream://d317a003e8047da2c36a2a2bb2289578c9a3b79c\n'

    channel_pattern = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO" ,CHANNELTITLE\nacestream://CHANNELID\n'
    channel_pattern_http = '#EXTINF:-1 group-title="GROUPTITLE" tvg-id="TVGID" tvg-logo="LOGO" ,CHANNELTITLE\nCHANNELID\n'

    for group_title in u.group_title_order:
        for channel_info in channel_list:
            if channel_info["group_title"] == group_title:
                if "http" in channel_info["channel_id"]:
                    ch_pattern = channel_pattern_http
                else:
                    ch_pattern = channel_pattern
                channel = ch_pattern.replace("GROUPTITLE", channel_info["group_title"]) \
                                               .replace("TVGID", channel_info["tvg_id"]) \
                                               .replace("LOGO", channel_info["logo"]) \
                                               .replace("CHANNELID", channel_info["channel_id"]) \
                                               .replace("CHANNELTITLE", channel_info["channel_name"])
                all_channels += channel
                #print(channel)

    if all_channels != "":
        
        all_channels_kodi = all_channels.replace("acestream://", "plugin://script.module.horus?action=play&id=")
        all_channels_get = all_channels.replace("acestream://", "http://127.0.0.1:6878/ace/getstream?id=")
        all_channels_int = all_channels.replace("acestream://", "http://192.168.1.90:8008/ace/getstream?id=")



        with open("base.txt", "w") as f:
            f.write(all_channels)
            print("exportChannels : OK : list exported")
            f.close()

        with open("kodi.txt", "w") as k:
            k.write(all_channels_kodi)
            print("exportChannels : OK : kodi list exported")
            k.close()

        with open("get.txt", "w") as g:
            g.write(all_channels_get)
            print("exportChannels : OK : get list exported")
            g.close()
            
        with open("int.txt", "w") as int:
            int.write(all_channels_int)
            print("exportChannels : OK : int list exported")
            int.close()
            
    else:
        print("exportChannels : ERROR : list is empty")
        

if __name__ == "__main__":
    main()
    #gitUpdate()
