'''
A helper class that talks to the imgflip API
'''
import os
import discord
import aiohttp
from stickord.registry import get_easy_logger

LOGGER = get_easy_logger('helpers.imgflip_api')

if not os.environ.get('IMGFLIP_USERNAME') or not os.environ.get('IMGFLIP_PASSWORD'):
    LOGGER.warning('No imgflip credentials set, using defaults.')
    LOGGER.warning('Default credentials may be subject to rate limiting.')

    IMGFLIP_UNAME = 'imgflip_hubot'
    IMGFLIP_PASS = 'imgflip_hubot'
else:
    IMGFLIP_UNAME = os.environ['IMGFLIP_USERNAME']
    IMGFLIP_PASS = os.environ['IMGFLIP_PASSWORD']

async def generate_meme(id, text_upper, text_bottom):
    ''' Generates a meme and returns the image link. '''
    url = 'https://api.imgflip.com/caption_image'
    params = {'username': 'imgflip_hubot',
              'password': 'imgflip_hubot',
              'template_id': id,
              'text0': text_upper,
              'text1' : text_bottom}
    async with aiohttp.post(url, params=params) as r:
        LOGGER.info('Doing imgflip POST request')
        return await r.json()


async def print_meme(meme):
    ''' Formats an imgflip response to be returned in an embed. '''
    embed = discord.Embed(color=discord.Color(0x666666))
    embed.set_image(url=meme['data']['url'])

    return embed


def get_meme_id(str):
    for key, val in meme_dict.items():
        if str in key:
            return val
    return 61520


meme_dict = {
'onedoesnotsimplyonedoesnotsimplywalkintomorderlordoftheringsboromir': '61579',
'batmanslappingrobin': '438680',
'ancientaliensgiorgiotsoukaloshistorychannelguy': '101470',
'futuramafrynotsureifxoryskepticalfry': '61520',
'themostinterestingmanintheworldidontalwaysbutwhenidodosequisman': '61532',
'xxeverywheredickseverywherewoodyandbuzzlightyearpointingtoystory': '347390',
'waitingskeletonskeletonwaitingonbenchinthepark': '4087833',
'leonardodicapriocheersthegreatgatsbypartywithjaygatsby': '5496396',
'firstworldproblemsfwpwomancrying': '61539',
'braceyourselvesxiscomingimminentnedfromgameofthronesbraceyourselveswinteriscomingbraceyourself': '61546',
'badluckbrian': '61585',
'yuno': '61527',
'thatwouldbegreatbilllumberghofficespaceyeathatdbegreat': '563423',
'oprahyougetaoprahgivewayoprahwinfreyoprahyougetacareveryonegetsacaryougetanoprahoprahexcited': '28251713',
'creepycondescendingwonkawillywonkastare': '61582',
'boardroommeetingsuggestionthrowaguyouttheboardroomwindow': '1035805',
'butthatsnoneofmybusinesskermitthefrogkermitdrinkingliptonicedtea': '16464531',
'dogeshibainu': '8072285',
'captainpicardfacepalmstartrekfacepalm': '1509839',
'yallgotanymoreofdavechapellechapellesshow': '13424299',
'successkidmotivationbabymotivationkidsuccessbaby': '61544',
'grumpycat': '405658',
'xalltheyallthethings': '61533',
'thirdworldskepticalkidafricanskepticalchild': '101288',
'matrixmorpheuswhatifitoldyou': '100947',
'blackgirlwatconfusedblackgirlblackgirlwithhandoutseriouslyblackgirl': '14230520',
'picardwtfcaptainjeanlucpicardstartrekannoyedpicardwhythefuckwouldyou': '245898',
'therockdriving': '21735',
'philosoraptorgreendinosaur': '61516',
'starwarsyodamasteryoda': '14371066',
'drevillaserdrevilquotationmarksdrevilairquotes': '40945639',
'faceyoumakerobertdowneyjr': '9440985',
'disastergirl': '97984',
'confessionbear': '100955',
'eviltoddlerevilbaby': '235589',
'findingneverlandjohnnydeppandlittlekidcrying': '6235864',
'grandmafindstheinternet': '61556',
'amitheonlyonearoundhereangrywalterfromthebiglebowski': '259680',
'10guyreallyhighguystonerstanleybrainwashedbob': '101440',
'toodamnhightherentistoodamnhigh': '61580',
'thirdworldsuccesskidhappyafricanchild': '101287',
'dontyousquidwardspongebob': '101511',
'awkwardmomentsealionawkwardsealuncomfortablesituationsealionheavybreathingsealion': '13757816',
'yodawgheardyouxzibityodawgweheardyoulikeysoweputsomexinyourxsoyoucanywhileyouy': '101716',
'mauryliedetectortheliedetectordeterminedthatwasaliethefactthatyouxdeterminedthatwasaliemaurypovich': '444501',
'aaaaanditsgoneanditsgonesouthparkbankerguy': '766986',
'spartaleonidasleonidasfromthemovie300': '195389',
'laughingmeninsuitsmenlaughingandthenisaidandthenitoldthemrichmenlaughing': '922147',
'skepticalbaby': '101711',
'aintnobodygottimeforthat': '442575',
'saythatagainidareyousamuelljacksonpulpfiction': '124212',
'putitsomewhereelsepatrickpatrickfromspongebob': '61581',
'conspiracykeanu': '61583',
'badpundogjokedogwhisperjokedoghappyhuskyjoketellinghuskypunhusky': '12403754',
'illjustwaitherewaitingskeleton': '109765',
'backinmydaygrumpyoldmanpointing': '718432',
'mugatusohotrightnowmugatufromzoolanderwillfarrell': '21604248',
'steveharvey': '143601',
'belikebillbillthestickfigurewithahat': '56225174',
'sociallyawesomeawkwardpenguin': '61584',
'andeverybodylosestheirmindsheathledgerjokerfromthedarkknight': '1790995',
'rickandcarlrheycarlrickgrimescryingthewalkingdeadheycarlwalkingdadjokesheycoral': '11557802',
'archerdoyouwantxbecausethatshowyougetxdoyouwantantsbecausethatshowyougetants': '10628640',
'spongegarcavemanspongebobsavagespongebobprimitivespongebobspongebobcaveman': '68690826',
'scumbagsteve': '61522',
'imaginationspongebobspongebobrainbownobodycares': '163573',
'thisiswhereidputmytrophyifihadone': '3218037',
'killyourselfguystopitguycorrectionguygrammarguy': '172314',
'arthurfistarthurhandarthursfistarthurshand': '74191766',
'pepperidgefarmremembers': '1232104',
'seenobodycaresjurassicparkdennis': '6531067',
'unclesamusamurica': '89655',
'ishouldbuyaboatcatsophisticatedcatfancycatnewspapercat': '1367068',
'liamneesontakeniwillfindyouandiwillkillyou': '228024',
'marvelcivilwar1captainamericavsironmantonystark': '28034788',
'lookatmeimthecaptainnowcaptainphillips': '29617627',
'buddychristbuddyjesusenthusiasticjesussmilinthumbsupjesus': '17699',
'jackiechanwtfwhatthef': '412211',
'unpopularopinionpuffin': '7761261',
'spidermancomputerdeskeveryoneisxandimjustsittinghereyretrospidermansitting': '1366993',
'overlyattachedgirlfriendlainawalkeroag': '100952',
'ryangoslingheygirl': '389834',
'petergriffinnewsfamilyguypetergriffinwhatreallygrindsmygears': '356615',
'shutupandtakemymoneyfryfuturamafrycashinhand': '176908',
'goodfellashilariousrayliottalaughing': '47235368',
'gollumsmeagol': '681831',
'leonardodicapriowolfofwallstreetleonardodicapriolaugh': '17496002',
'ermahgerdberksgersberms': '101462',
'itsnotgoingtohappenmeangirlsreginageorge': '10364354',
'hidethepainharoldsadlifeharoldmaurice': '27813981',
'davechappelleyallgotanymoreofthatstufftyronebiggums': '36061805',
'memberberriesrememberwhenmemberberry': '78381262',
'suddenclarityclarence': '100948',
'cutecatcutekittenstandingup': '8279814',
'spidermanpeterparkertobeymaquiresneakysidewaysglancespiderman': '107773',
'obiwankenobi': '409403',
'surprisedkoalasurprisedkoalabeareatingleaves': '27920',
'kevinhartthehellwhatchalookinat': '265789',
'imthecaptainnowcaptainphillipslookatme': '29562797',
'youtherealmvpkevindurantyoudarealmvp': '15878567'
}