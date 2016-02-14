# -*- coding: utf-8 -*-
import Patterns.Pattern as Pattern
import Patterns.Function as Function
import Patterns.StaticPatterns.basicPatterns
import Patterns.ExtraPatterns.SimpleText
import Patterns.ExtraPatterns.Image
import SavedFunctions



def importFunctionsFromDict(dictionary):
    for functionName in dictionary:
        globals()[functionName] = dictionary[functionName]

importFunctionsFromDict(Pattern.getPatternDic())
importFunctionsFromDict(Function.getFunctionDict())
importFunctionsFromDict(Function.getMetaFunctionDict())

rotatingRainbow=Pattern.pattern('rotatingRainbow')(isolateCanvas(step(rainbow,vRainbownize(trivial))))

coolRandom=Pattern.pattern('coolRandom')(movingHue(constant(random)))

movingColors=Pattern.pattern('movingColors')(movingHue(red))
prettyDiagonalRainbow=Pattern.pattern('prettyDiagonalRainbow')(defaultArgs(hueFrameRate=0.02, nVRainbows=3, nRainbows=2)(compose(movingHue,vRainbownize,rainbownize))(red))

softRainbow=Pattern.pattern('softRainbow')(movingHue(meanP(movingColors,rainbow)))

rainbowAurora = Pattern.pattern('rainbowAurora')(isolateCanvas(movingHue(meanP(step(softRainbow,vRainbownize(trivial)),softRainbow))))

_pulsatingCircle = Pattern.pattern('_pulsatingCircle')(arg('cRadius=abs(frame%20-10)/10.')(circle))

_explosionRed = Pattern.pattern('_explosionRed')(arg('cRadius = sin(frame/30.)*4./3.; hue=0.05')(mask(circle,hueShift(trivial),meanP(red,trivial))))
meteorRainbow = Pattern.pattern('meteorRainbow')(arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2 ')(mask(translate(circle),meanP(softRainbow,trivial),blur(trivial))))
_mesmerezingMeteor = Pattern.pattern('_mesmerezingMeteor')(isolateCanvas(hueShift((arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2; weightedMeanWeight=0.05; hue=0.021')(mask(translate(circle),prettyDiagonalRainbow, weightedMean2P(black,blur(trivial))))))))

cloudsRainbow = Pattern.pattern('cloudsRainbow')(arg('generationBornRange=[3,4]; generationSurviveRange=[1,2,3]; generationStates=48; generationNeighborDistance=1 ')(isolate(step(circle,gameOfGeneration(trivial)))))

spaaceMoving = Pattern.pattern('spaaceMoving')(arg('textHeight=0.2; textPos=0.5; xTranslate= frame%17/17.; yTranslate=frame%33/33.; weightedMeanWeight=0 if frame%10==0 else 1')(step(black,mask(isolateCanvas(step(black,weightedMean2P(trivial,translate(text)))),softRainbow,arg('weightedMeanWeight=0.1 ')(weightedMean2P(black,blur(trivial)))))))

scrollingText = Pattern.pattern('scrollingText')(arg('textPos=frame%float(len(text)*8)/(len(text)*8) ')(text))

vladTheImpaler = Pattern.pattern('vladTheImpaler')(isolate(arg("""text ='''  Vlad the Impaler From Wikipedia, the free encyclopedia Changes must be reviewed before being displayed on this page.show/hide details "Vlad Țepeș" redirects here. For other uses, see Vlad Țepeș (disambiguation). Vlad III Dracula Владъ Цепѣшъ Vlad Tepes 002.jpg The Ambras Castle portrait of Vlad III, c. 1560, reputedly a copy of an original made during his lifetime.[1] Voivode of Wallachia Reign 1448; 1456–1462; 1476 Born November or December 1431[1] Segesvár, Kingdom of Hungary (city now known as Sighișoara, Romania) Died December 1476 or January 1477, exact date unknown (aged 44–45) Wallachia (exact location unknown) Wives Transylvanian noblewoman Ilona Szilágyi Issue Mihnea cel Rău, Vlad IV, and Mircea (disputed name) House House of Drăculești (branch of the House of Basarab) Father Vlad II Dracul Mother Cneajna of Moldavia (presumed) Signature Vlad III, Prince of Wallachia (1431–1476/77), was a member of the House of Drăculești, a branch of the House of Basarab, also known, using his patronymic, as Vlad Drăculea or Vlad Dracula (Old Church Slavonic: Владъ Дрьколъ). He was posthumously dubbed Vlad the Impaler (modern Romanian: Vlad Țepeș, pronounced [ˈvlad ˈt͡sepeʃ]) He was a three-time Voivode of Wallachia, ruling mainly from 1456 to 1462, the period of the incipient Ottoman conquest of the Balkans. His father, Vlad II Dracul, was a member of the Order of the Dragon, which was founded to protect Christianity in Eastern Europe. Vlad III is revered as a folk hero in Romania and Bulgaria for his protection of the Romanians and Bulgarians both north and south of the Danube. Following his raids on the Ottomans, a significant number of Bulgarian common folk and remaining boyars resettled north of the Danube to Wallachia and recognized his leadership.[1] As the cognomen "The Impaler" suggests, his practice of impaling his enemies is part of his historical reputation.[2] During his lifetime, his reputation for excessive cruelty spread abroad, to Germany and elsewhere in Europe. The name of the vampire Count Dracula in Bram Stoker's 1897 novel Dracula was inspired by Vlad's patronymic and reputation.[2] Contents [hide] 1 Name 2 Early life 2.1 Family 2.2 Dealings with the Ottoman Empire and first reign (1448) 3 Second and main reign (1456–62) 3.1 War with the Ottomans 3.1.1 Sultan Mehmed II's invasion of Wallachia 4 Defeat 4.1 Imprisonment in Hungary 5 Reconquest of Wallachia, Third reign and death 5.1 Burial 6 Legacy 6.1 Reputation for cruelty 6.2 German sources 6.3 Russian sources 6.4 Ambras Castle portrait 6.5 Romanian patriotism 6.6 Vampire mythology 7 See also 8 References 9 External links Name[edit] Further information: House of Drăculești Bust of Vlad the Impaler in Sighișoara, his place of birth During his life, Vlad wrote his name in Latin documents as Wladislaus Dragwlya, vaivoda partium Transalpinarum (1475).[3] His Romanian patronymic Dragwlya (or Dragkwlya)[3] Dragulea, Dragolea, Drăculea,[4][5] is a diminutive of the epithet Dracul carried by his father Vlad II, who in 1431 was inducted as a member of the Order of the Dragon, a chivalric order founded by Emperor Sigismund in 1408. Dracul is the Romanian definite form, the -ul being the suffixal definite article (deriving from Latin ille). The noun drac "dragon" itself continues Latin draco. In Modern Romanian, the word drac has adopted the meaning of "devil" (the term for "dragon" now being balaur or dragon). This has led to misinterpretations of Vlad's epithet as characterizing him as "devilish". Vlad's nickname of Țepeș ("Impaler") identifies his favourite method of execution but was only attached to his name posthumously, in c. 1550.[3] Before this, however, he was known as Kaziklu Beg or Kaziklı Voyvoda (both meaning : Impaler Lord) by the Ottoman Empire after their armies encountered his "forests" of impaled victims.[6] Early life[edit] Family[edit] Vlad was born in Sighișoara, Voivodeship of Transylvania, Kingdom of Hungary (today part of Romania), in the winter of 1431, to Vlad II Dracul, future voivode of Wallachia. Vlad's father was the son of the celebrated Voivode Mircea the Elder. His mother is unknown, though at the time his father was believed to have been married to Princess Cneajna of Moldavia (eldest daughter of Alexander "the Good", Prince of Moldavia and aunt to Stephen the Great of Moldavia) and also to have kept a number of mistresses.[1] He had two older half-brothers, Mircea II and Vlad Călugărul, and a younger brother, Radu III the Handsome. Vlad had a half-brother also named Vlad through his father's mistress Caltuna. She entered a monastery and her son followed in her footsteps to become Vlad the Monk. [7] Vlad Dracul In the year of his birth, Vlad's father traveled to Nuremberg, where he was then vested into the Order of the Dragon,[1] a fellowship of knights sworn to defend Christendom against the encroaching Ottomans and European heresies, such as the Hussites.[8] During his initiation, he was given the epithet Dracul, or dragon, by the Holy Roman Emperor Sigismund.[9] Vlad and Radu spent their early formative years in Sighișoara. During the first reign of their father, Vlad II Dracul, the Voivode brought his young sons to Târgoviște, the capital of Wallachia at that time. The Byzantine chancellor Mikhail Doukas showed that, at Târgoviște, the sons of boyars and ruling princes were well-educated by Romanian or Greek scholars commissioned from Constantinople. Vlad is believed to have learned combat skills, geography, mathematics, science, languages (Old Church Slavonic, German, Latin), and the classical arts and philosophy. Dealings with the Ottoman Empire and first reign (1448)[edit] In 1436, Vlad II Dracul ascended the throne of Wallachia. He was ousted in 1442 by rival factions in league with Hungary, but secured Ottoman support for his return by agreeing to pay tribute to the Sultan.[citation needed]. Vlad II Dracul also agreed to let two of his sons stay at the Ottoman court as an extra guarantee, that he remained loyal to the Ottoman Sultan.[2][10] At 11 in 1442, Vlad II Dracul was beguiled into a confrontation with Sultan Mehmed II. Insensitive to the situation, Vlad II Dracul took his two sons Mercea and Dracula to meet him, only for them to be taken prisoner. During his years as "favoured prisoner" in Gallipolli, Vlad was educated in logic, the Quran, and the Turkish language and works of literature. He would speak this language fluently in his later years.[1] [11]He and his brother were also trained in warfare and horsemanship.[12] It is suspected that the young Dracula spent some time in 1443 in Constantinople in the court of Constantine XI Paleologus, the final Emperor of the Byzantine Empire. Both were eventually released in 1448 after 6 years of "captivity". His Turkish allies supported him by attempting to install him as Voivode of Wallachia. This bold coup lasted two months when his opponents were distracted. Vlad was not at all pleased to be in Turkish hands. He was resentful and very jealous of his little brother, who soon earned the nickname Radu cel Frumos, or "Radu the Handsome". Radu was well behaved and quickly earned the friendship of Sultan Murad's son, Mehmet; he eventually converted to Islam and entered Ottoman service.[13] Conversely, Vlad was defiant and constantly punished for his impudence. It has been suggested that his traumatic experiences among the Ottomans may have molded him into the sadistic man he grew up to be, especially in regards to his penchant for impaling.[8] The death of Vlad's father Vlad II Dracul and older-half-brother Micea, both politically assassinated, greatly contributed to the development of the sadistic nature of Dracula.[12][14] After his escape, Dracula escaped to Moldova, fearful of assassins, to learn under the tutelage of his uncle Prince Bogdan and his cousin Prince Stephen. They formed a close friendship, promising each other to help other in need. This was called into action in 1457 when Vlad helped his cousin Stephen ascend Moldavia's throne by providing 6,000 horsemen as military assistance against Petru Aron, who was deposed after two battles. Stephen of Moldavia's long lasting reign developed into the most fierce anti-Ottoman resistance.[15] In 1451, only three years after his "adoption", Dracula was forced to flee due to Prince Bogdan's assassination. He reappeared in Transylavnia and put himself under the tutelage of the mighty Hungarian miliary leader Janos Hunyadi and the Hungarian king Ladislaus. Under their tutelage, Dracula learned immensely. It was in 1456 that Dracula was sent to eliminate the Turkish-friendly Vladislav II, who was the Voivode of Wallachia. Dracula came to the throne as his main and important reign. [12] Second and main reign (1456–62)[edit] With Hungarian help, Vlad took the throne of Wallachia from Vladislav II in 1456. In 1457 exactly a year after ascension, Vlad helped his cousin Stephen ascend Moldavia's throne by providing 6,000 horsemen as military assistance against Petru Aron, who was deposed after two battles. Stephen of Moldavia's long lasting reign developed into the most fierce anti-Ottoman resistance.[15] War with the Ottomans[edit] Vlad the Impaler and the Turkish Envoys. Painting by Theodor Aman. In 1459, Pope Pius II called for a new crusade against the Ottomans, at the Congress of Mantua. In this crusade, the main role was to be played by Matthias Corvinus, son of John Hunyadi (János Hunyadi), the King of Hungary. To this effect, Matthias Corvinus received from the Pope 40,000 gold coins, an amount that was thought to be enough to gather an army of 12,000 men and purchase 10 Danube warships. In this context, Vlad allied himself with Matthias Corvinus, with the hope of keeping the Ottomans out of the country (Wallachia was claimed as a part of the Ottoman Empire by Sultan Mehmed II). Later that year, 1459, Ottoman Sultan Mehmed II sent envoys to Vlad to urge him to pay a delayed tribute[16] of 10,000 ducats and 500 recruits into the Ottoman forces. Vlad refused, because if he had paid the 'tribute', as the tax was called at the time, it would have meant a public acceptance of Wallachia as part of the Ottoman Empire. Vlad, like most of his predecessors and successors, maintained the goal of keeping Wallachia independent. Vlad had the Turkish envoys killed on the pretext that they had refused to raise their "hats" to him, by nailing their turbans to their heads. Meanwhile, the Sultan received intelligence reports that revealed Vlad's domination of the Danube. He sent the Bey of Nicopolis, Hamza Bey (also known as Hamza Ceakirdjiba), to make peace and, if necessary, eliminate Vlad III. Vlad Țepeș planned to set an ambush. Hamza Bey, the Bey of Nicopolis, brought with him 1000 cavalry and when passing through a narrow pass north of Giurgiu, Vlad launched a surprise attack. The Wallachians had the Turks surrounded and defeated. The Turks' plans were thwarted and almost all of them caught and impaled, with Hamza Bey impaled on the highest stake to show his rank. The Night Attack of Târgovişte, which resulted in the victory of Vlad the Impaler. In the winter of 1462, Vlad crossed the Danube and devastated the entire Bulgarian land in the area between Serbia and the Black Sea. Disguising himself as a Turkish Sipahi and utilizing the fluent Turkish he had learned as a hostage, he infiltrated and destroyed Ottoman camps. In a letter to Corvinus dated 2 February, he wrote:[17] I have killed peasants men and women, old and young, who lived at Oblucitza and Novoselo, where the Danube flows into the sea... We killed 23,884 Turks without counting those whom we burned in homes or the Turks whose heads were cut by our soldiers...Thus, your highness, you must know that I have broken the peace. Sultan Mehmed II's invasion of Wallachia[edit] In response to this, Sultan Mehmed II raised an army of around 60,000 troops and 30,000 irregulars, and in spring of 1462 headed towards Wallachia. This army was under the Ottoman general Mahmut Pasha and in its ranks was Radu. Vlad was unable to stop the Ottomans from crossing the Danube on 4 June 1462 and entering Wallachia. He constantly organized small attacks and ambushes on the Turks, such as The Night Attack when 15,000 Ottomans were killed.[1] This infuriated Mehmed II, who then crossed the Danube. Radu was left behind in Târgoviște with the hope that he would be able to gather an anti-Vlad clique in Wallachia that would ultimately establish Radu as the new Voivode of the region. Vlad's rule falls entirely within the three decades of the Ottoman conquest of the Balkans, conquering the entire Balkans peninsula. Vlad the Impaler's attack was celebrated by the Saxon cities of Transylvania, the Italian states and the Pope. A Venetian envoy, upon hearing about the news at the court of Corvinus on 4 March, expressed great joy and said that the whole of Christianity should celebrate Vlad Țepeș's successful campaign. The Genoese from Caffa also thanked Vlad, for his campaign had saved them from an attack of some 300 ships that the sultan planned to send against them.[18] Defeat[edit] Writ issued on 14 October 1465 by Radu cel Frumos, from his residence in Bucharest signified the victory of the Ottoman Empire. Vlad's initial victory against the Ottomans was short-lived and he soon withdrew to Moldavia leaving behind detachments in Wallachia that were overrun by the Ottoman Sipahi commander Turhanoghlu Omer Bey, who was rewarded by being appointed governor of Thessaly. Vlad's younger brother Radu cel Frumos and his Janissary battalions were given the task by the Ottoman administrator Mihaloghlu Ali Bey on behalf of the Sultan, of leading the Ottoman Empire to victory. As the war raged on, Radu and his formidable Janissary battalions were well supplied with a steady flow of gunpowder and dinars; this allowed them to push deeper into the realm of Vlad III. Radu's forces finally besieged Poenari Castle, the famed lair of Vlad III. After his victory Radu was given the title Bey of Wallachia by Sultan Mehmed II. Vlad III's defeat at Poenari was due in part to the fact that the Boyars, who had been alienated by Vlad's policy of undermining their authority, had joined Radu under the assurance that they would regain their privileges. They may have also believed that Ottoman protection was better than Hungarian. By September 8, Vlad had won another three victories, but continuous war had left him without any money and he could no longer pay his mercenaries.[citation needed] Imprisonment in Hungary[edit] In autumn of 1462, Vlad and Matthias Corvinus spent five weeks negotiating alliances and battle plans at Braşov. After believing he had gained Hungarian support for his crusade against the Ottomans, a confident Vlad started on his way home to Wallachia. Unbeknownst to him, there was an ambush waiting for him at Castle King's Rock, a fortress about six kilometers north of Rucăr, barely inside the Wallachian state. On November 26, Vlad was captured by Matthias Corvinus' own men and spirited away to Hungary.[19] Transylvanian Saxon engraving from 1462 depicting Vlad Țepeș Neither his contemporaries nor modern day scholars can say why exactly Matthias Corvinus shifted his loyalties and betrayed Vlad. Relatively recent research volunteers a possible explanation, though: In the early 1460s, the Hungarian king became distracted by the possibility of receiving the title of Holy Roman Emperor, and effectively tried to end the anti-Ottoman crusades in Eastern Europe. To focus on gaining power in Central Europe, he abandoned the Balkans to the Turks, a hasty and incriminating move for a supposed crusader-king. In order to justify his actions, he ordered Vlad's arrest, claiming that the Wallachian prince was actually in league with the Turks;[19] therefore, the entire area was undeserving of his protection. Vlad was imprisoned at the Oratea Fortress located at today's Podu Dâmboviței village. A period of imprisonment in Visegrád near Buda followed. The exact length of Vlad's period of imprisonment is open to some debate, though indications show that it was from 1462 until 1466.[20] Diplomatic correspondence from Buda seems to indicate that the period of Vlad's effective confinement was relatively short, his release occurring around 1466 when he married Ilona Szilágyi.[21] Radu's openly pro-Ottoman policy as voivode probably contributed to Vlad's rehabilitation. Moreover, Ștefan cel Mare, Voivode of Moldavia and relative of Vlad, intervened on his behalf to be released from prison as the Ottoman pressure on the territories north of the Danube was increasing. Reconquest of Wallachia, Third reign and death[edit] Around 1475 Vlad began preparations for the reconquest of Wallachia with Stephen V Báthory of Transylvania, mixed forces of Transylvanians, Hungarian support, some dissatisfied Wallachian boyars, and Moldavians sent by Prince Stephen III of Moldavia, Vlad's cousin. Vlad's brother, Radu the Handsome, had died many years earlier and had been replaced on the Wallachian throne by another Turkish candidate, Prince Basarab the Elder, a member of the Dăneşti clan. When Vlad's army arrived, Prince Basarab's army fled, some to the Turks, others in the mountains. After placing Vlad on the throne, Stephen Báthory and his forces returned to Transylvania, leaving Vlad in a very weak position. Vlad had little time to get support before a large Turkish army entered Wallachia to put Prince Basarab back on the throne. Vlad had to meet the Turks with the small forces at his disposal, which were made up of fewer than four thousand men. Vlad III declared his third reign in 26 November 1476, where it had lasted little more than two months and thereafter he was killed. [22] There are five variants of Vlad's death. Some sources[who?] say he was killed while fighting the Turks, surrounded by the bodies of his loyal Moldavian bodyguards. Others say he was killed by disloyal Wallachian boyars also fighting the Turks, or killed during a hunt. Still other reports claim that Vlad was accidentally killed by one of his own men. The exact date and location of Vlad's death are unknown, but he was dead by 10 January 1477. He is presumed to have died at the end of December 1476, somewhere along the road between Bucharest and Giurgiu.[10] According to Bonfinius (Antonio Bonfini) and a Turkish chronicler,[23] Vlad was decapitated by the Turks as a trophy, and his head was sent to Constantinople (now Istanbul), preserved in honey. After, the head was displayed on a stake as proof that he was dead. Burial[edit] Vlad's body was buried unceremoniously by his rival, Basarab Laiota, possibly at Comana, a monastery founded by Vlad in 1461.[24] The Comana monastery was demolished and rebuilt from scratch in 1589.[25] In the 19th century, Romanian historians cited a "tradition", apparently without any kind of support in documentary evidence, that Vlad was buried at Snagov, an island monastery located near Bucharest. To support this theory, the so-called Cantacuzino Chronicle was cited, which cites Vlad as the founder of this monastery, but as early as 1855, Alexandru Odobescu had established that this is impossible as the monastery had been in existence before 1438. Since excavations carried out by Dinu V Rosetti in June– October 1933, it has become clear that Snagov monastery was founded during the later 14th century, well before the time of Vlad III. The 1933 excavation also established that there was no tomb below the supposed "unmarked tombstone" of Vlad in the monastery church. Rosetti (1935) reported that "Under the tombstone attributed to Vlad there was no tomb. Only many bones and jaws of horses." In the 1970s, speculative attribution of an anonymous tomb found elsewhere in the church to Vlad Țepeș was published by Simion Saveanu, a journalist who wrote a series of articles on the occasion of the 500th anniversary of Vlad's death.[25] Most Romanian historians today favor the Comana monastery as the final resting place for Vlad Țepeș.[24] Legacy[edit] Reputation for cruelty[edit] Pilate Judging Jesus Christ, National Gallery, Ljubljana, 1463. The Martyrdom of Saint Andrew (1470–1480, Belvedere Galleries) Paintings such as these are said to depict Biblical tyrants with the features of Vlad. Above, as Pontius Pilate, below as a Roman proconsul After Vlad's death, his deeds were reported in popular pamphlets in Germany, reprinted from the 1480s until the 1560s, and to a lesser extent in Tsarist Russia. A typical German pamphlet from 1521 gives numerous examples of lurid incidents, such as the following:[26] He roasted children, whom he fed to their mothers. And (he) cut off the breasts of women, and forced their husbands to eat them. After that, he had them all impaled.[26] Vlad Ţepeş's reputation was considerably darker in western Europe than in eastern Europe and Romania. In the West, Vlad III Ţepeş has been characterized as a tyrant who took sadistic pleasure in torturing and killing his enemies.[27] Estimates of the number of his victims range from 40,000 to 100,000.[28] He also had whole villages and fortresses destroyed and burned to the ground.[29] Impalement was Vlad's preferred method of torture and execution. Several woodcuts from German pamphlets of the late 15th and early 16th centuries show Vlad feasting in a forest of stakes and their grisly burdens outside Brașov, while a nearby executioner cuts apart other victims.[30] It has also been said that in 1462 Mehmed II, the conqueror of Constantinople, returned to Constantinople after being sickened by the sight of 20,000 impaled corpses outside Vlad's capital of Târgoviște.[31] German sources[edit] 1499 German woodcut showing Dracule waide dining among the impaled corpses of his victims. The German stories circulated first in manuscript form in the late 15th century and the first manuscript was probably written in 1462 before Vlad's arrest. The text was later printed in Germany and had a major impact on the general public, becoming a bestseller of its time with numerous later editions adding to and altering the original text. In addition to the manuscripts and pamphlets the German version of the stories can be found in the poem of Michael Beheim. The poem called "Von ainem wutrich der hies Trakle waida von der Walachei" ("Story of a Hothead Named Dracula of Wallachia") was written and performed at the court of Frederick III, Holy Roman Emperor during the winter of 1463.[32] To this day four manuscripts and 13 pamphlets have been found, as well as the poem by Michel Beheim. The surviving manuscripts date from the last quarter of the 15th century to the year 1500 and the found pamphlets date from 1488 to 1559–1568. Eight of the pamphlets are incunabula, meaning that they were printed before 1501. The German stories about Vlad the Impaler consist of 46 short episodes, although none of the manuscripts, pamphlets or the poem of Beheim contain all 46 stories. All of them begin with the story of the old governor, John Hunyadi, having Vlad's father killed, and how Vlad and his brother renounced their old religion and swore to protect and uphold the Christian faith. After this, the order and titles of the stories differ by manuscript and pamphlet editions.[29] Russian sources[edit] The Russian or the Slavic version of the stories about Vlad the Impaler called "Skazanie o Drakule voevode" ("The Tale of Warlord Dracula") is thought to have been written sometime between 1481 and 1486. Copies were made from the 15th century to the 18th century, of which some 22 extant manuscripts survive in Russian archives.[33] The oldest one, from 1490, ends as follows: "First written in the year 6994 of the Byzantine calendar (1486), on 13 February; then transcribed in the year 6998 (1490), on 28 January". The Tales of Prince Dracula is neither chronological nor consistent, but mostly a collection of anecdotes of literary and historical value concerning Vlad Țepeș. There are 19 anecdotes in The Tales of Prince Dracula which are longer and more constructed than the German stories. The Tales can be divided into two sections: The first 13 episodes are non-chronological events most likely closer to the original folkloric oral tradition about Vlad. The last six episodes are thought to have been written by a scholar who collected them, because they are chronological and seem to be more structured. The stories begin with a short introduction and the anecdote about the nailing of hats to ambassadors' heads. They end with Vlad's death and information about his family.[citation needed] Of the 19 anecdotes there are ten that have similarities to the German stories.[34] Although there are similarities between the Russian and the German stories about Vlad, there is a clear distinction in the attitude towards him. The Russian stories tend to portray him in a more positive light: he is depicted as a great ruler, a brave soldier and a just sovereign. Stories of atrocities tend to seem to be justified as the actions of a strong ruler. Of the 19 anecdotes, only four seem to have exaggerated violence.[citation needed] Some elements of the anecdotes were later added to Russian stories about Ivan the Terrible of Russia.[35] The nationality and identity of the original writer of the Dracula anecdotes are disputed. The two most plausible explanations are that the writer was either a Romanian priest or a monk from Transylvania, or a Romanian or Moldavian from the court of Stephen the Great in Moldavia. One theory claims the writer was a Russian diplomat named Fyodor Kuritsyn.[36] Ambras Castle portrait[edit] A contemporary portrait of Vlad III, rediscovered by Romanian historians in the late 19th century, had been featured in the gallery of horrors at Innsbruck's Ambras Castle. This original has been lost to history, but a larger copy, painted anonymously in the first half of the 16th century, now hangs in the same gallery.[1] This copy, unlike the crypto-portraits contemporary with Vlad III, seems to have given him a Habsburg lip.[37] Romanian patriotism[edit] This section needs additional citations for verification. Please help improve this article by adding citations to reliable sources. Unsourced material may be challenged and removed. (November 2015) Further information: Romanian national awakening Romanian and Bulgarian documents from 1481 onwards portray Vlad as a hero, a true leader, who used harsh yet fair methods to reclaim the country from the corrupt and rich boyars. Moreover, all his military efforts were directed against the Ottoman Empire which explicitly wanted to conquer Wallachia. Excerpt from "The Slavonic Tales": And he hated evil in his country so much that, if anyone committed some harm, theft or robbery or a lye or an injustice, none of those remained alive. Even if he was a great boyar or a priest or a monk or an ordinary man, or even if he had a great fortune, he couldn't pay himself from death. [citation needed] A woodcut depicting Vlad Țepeș published in Nuremberg in 1488 on the title page of the pamphlet Die geschicht Dracole waide. An Italian writer, Michael Bocignoli from Ragusa, in his writings from 1524, refers to Vlad Țepeș as: It was once (in Valahia), a prince Dragul by his name, a very wise and skillful man in war. [38] (In Latin in the original text: Inter eos aliquando princeps fuit, quem voievodam appellant, Dragulus nomine, vir acer et militarium negotiorum apprime peritus.)[39] In the Letopisețul cantacuzinesc ("Cantacuzino chronicle"), a historic account written around 1688 by Stoica Ludescu of the Cantacuzino family, Vlad orders the boyars to build the fortress of Poenari with their own bare hands. Later in the document, Ludescu refers to the (re)crowning of Vlad as a happy event: Voievod Vlad sat on the throne and all the country came to pay respect, and brought many gifts and they went back to their houses with great joy. And Voievod Vlad with the help of God grew into much good and honor as long as he kept the reign of those just people. [citation needed] (In Romanian in the original text: De aciia șăzu în scaun Vladul-vodă și veni țara de i să închină, și aduse daruri multe și să întoarseră iarăși cine pre la case-și cu mare bucurie. Iar Vladul-vodă cu ajutorul lui Dumnezeu creștea întru mai mari bunătăți și în cinste pân' cât au ținut sfatul acelui neam drept.) Around 1785, Ioan Budai-Deleanu, a Romanian writer and renowned historian, wrote a Romanian epic heroic poem, "Țiganiada", in which prince Vlad Țepeș stars as a fierce warrior fighting the Ottomans. Later, in 1881, Mihai Eminescu, one of the greatest Romanian poets, in "Letter 3", popularizes Vlad's image in modern Romanian patriotism, having him stand as a figure to contrast with presumed social decay under the Phanariotes and the political scene of the 19th century. The poem even suggests that Vlad's violent methods be applied as a cure. In the final lyrics, the poet makes a call to Vlad Țepeș (i. e. Dracula) to come, to sort the contemporaries into two teams: the mad and the wicked and then set fire to the prison and to the madhouse.[40][better source needed] (In Romanian in the original text: Dar lăsaţi măcar strămoşii ca să doarmă-n colb de cronici; Din trecutul de mărire v-ar privi cel mult ironici. Cum nu vii tu, Ţepeş doamne, ca punând mâna pe ei, Să-i împarţi în două cete: în smintiţi şi în mişei, Şi în două temniţi large cu de-a sila să-i aduni, Să dai foc la puşcărie şi la casa de nebuni!) In contrast, documents of Germanic, Saxon, and Hungarian origin portray Vlad as a tyrant, a monster so cruel that he needs to be stopped. For example, Johan Christian Engel characterizes Vlad as "a cruel tyrant and a monster of humankind".[citation needed] Several authors and historians believe that this may be the result of a bad image campaign initiated by the Transylvanian Saxons who were actively persecuted during Vlad's reign and later maintained and spread by Matthias Corvinus. It is conceivable that these actions were not beyond the Hungarian king since he had already framed Vlad Țepeș by producing a forged letter to incriminate Vlad of coalition with the Turks. However, there is incontestable evidence, both in Romanian and foreign documents, including Vlad's own letters, that he killed tens of thousands of people in horrible ways.[citation needed] Vampire mythology[edit] See also: Dracula The connection of the name "Dracula" with vampirism was made by Bram Stoker around the 1890s[41] Since then, "Count Dracula" has been a recurring character in vampire mythology and popular culture'''""")(scrollingText)))

_nyanCat = Pattern.pattern('_nyanCat')(arg('imageName="nyanCatLarge" ')(image))

_crazyNyanPacman = Pattern.pattern('_crazyNyanPacman')(arg('imageHeight=imageWidth=0.5; xTranslate=-frame/30.; yTranslate=sin(frame/30.) ')(translate(addP(_nyanCat, arg('xTranslate=0.5')(translate(_nyanCat)), arg('yTranslate=0.5')(translate(_nyanCat)), arg('xTranslate=-yTranslate ')(translate(image)), arg('yTranslate=-xTranslate ')(translate(image))))))

_beatCircleRainbow = Pattern.pattern('_beatCircleRainbow')(arg('cRadius=(1-beat)*2;hue=totalBeats%4/4.;weightedMeanWeight=0.25')(hueShift(mask(circle, blue,weightedMean2P(rainbow,black)))))
_beat4Rainbow = Pattern.pattern('_beat4Rainbow')(arg('''hue=totalBeats%4/4. ''')(hueShift(constant(rainbow))))
_blueExplosion = Pattern.pattern('_blueExplosion')(arg('''gradientPos=-frame/30. ''')(radialHueGradient))
_beatBlueGradient = Pattern.pattern('_beatBlueGradient')(arg('''radialGradientPos=-beat; radialGradientColor0=0x0a000F; radialGradientColor1=0x0ffff ''')(radialHueGradient))
_gameOfLife = Pattern.pattern('_gameOfLife')(isolateCanvas(step(random, gameOfLife(trivial))))
_gameOfGenerations = Pattern.pattern('_gameOfGenerations')(isolateCanvas(step(random,gameOfGeneration(trivial))))

_hypnoCalm = Pattern.pattern('_hypnoCalm')(arg('''radialGradientRadius=(sin(frame/70.)+1)*3; radialGradientPos=sin(-frame/40.);radialGradientColor0=0xF0007 ''')(radialHueGradient))
_mazeGame = Pattern.pattern('_mazeGame')(arg('lifeSurviveRange=[2,3,4]; lifeBornRange=[3]')(_gameOfLife))
_beatCircleColor = Pattern.pattern('_beatCircleColor')(__hueShift4Beat(_beatBlueGradient))

_demo = Pattern.pattern('_demo')(arg('textHeight=0.3;timeChangerTime=30; transitionRandomPixels=10 ')(mask(vladTheImpaler,green,timeChanger(cloudsRainbow, transitionRandom(_mesmerezingMeteor), transitionRandom(rainbowAurora), _gameOfLife, transitionFade(_hypnoCalm), transitionRandom(arg('xTranslate = -frame/60. ')(translate(_nyanCat))), transitionFade(coolRandom),transitionRandom(_beatBlueGradient)))))

_nyanOnFire = Pattern.pattern('_nyanOnFire')(arg('weightedMeanWeight=0.65')(weightedMean2P(arg('imageName="fire"')(image),arg('imageName="nyanC";xTranslate=-frame/90. ')(translate(image)))))
_nyanFadeFire = Pattern.pattern('_nyanFadeFire')(arg('transitionRandomPixels=3; timeChangerTime=35; weightedMeanWeight=0.65')(weightedMean2P(arg('imageName="fire"')(timeChanger(image,image,transitionRandom(black))) ,arg('imageName="nyanC";xTranslate=-frame/90. ')(timeChanger(translate(image),translate(transitionRandom(black)), black)))))
_3rgbCircle = Pattern.pattern('_3rgbCircle')(defaultArgsP(trans0=0,trans1=0.333, trans2= -0.333, c0=0.666, c1=0.666, c2 =0.666)((addP(arg('xTranslate=trans0; cRadius=c0')(translate(circle)), arg('xTranslate=trans1; hue=0.333;cRadius=c1')(hueShift(translate(circle))),arg('xTranslate=trans2;hue=0.667;cRadius=c2')(hueShift(translate(circle)))))))
_beat3rgbCircle = Pattern.pattern('_beat3rgbCircle')(arg('''c1=(beat-.5)*2.;c0=beat*2.; c2=(beat-0.5)*2 ''')(defaultArgsP(trans0=0,trans1=0.333, trans2= -0.333, c0=0.666, c1=0.666, c2 =0.666)((addP(arg('xTranslate=trans0; cRadius=c0')(translate(circle)), arg('xTranslate=trans1; hue=0.333;cRadius=c1')(hueShift(translate(circle))),arg('xTranslate=trans2;hue=0.667;cRadius=c2')(hueShift(translate(circle))))))))
_beatBlueGradient3 = Pattern.pattern('_beatBlueGradient3')(defaultArgsP(radialGradientRadius=2)(mask(_beat3rgbCircle,_beatBlueGradient,black)))
_exampleEquationPlotter = Pattern.pattern('_exampleEquationPlotter')(arg('''equationAngle0=abs(sin(frame/90.)) ''')(equationxyPlotter))
_beatLinearHue3Circle = Pattern.pattern('_beatLinearHue3Circle')(arg('''linearGradientAngle=totalBeats/2.; linearGradientPos=beat ''')(mask(_beat3rgbCircle,linearHueGradient,black)))

_beatSinwave = Pattern.pattern('_beatSinwave')(arg('''equationX=str(2*(abs(1-totalBeats%2)-0.5))+'*sin(x)'; equationXxmin=-0.1*frame;  equationXxmax=equationXxmin+6 ''')(equationxPlotter))

_beatSinWaveTrail = Pattern.pattern('_beatSinWaveTrail')(isolateCanvas(arg('weightedMeanWeight=0.1 ')(addP(__beatInt4Hue(_beatSinwave),blur(weightedMean2P(black,trivial))))))
_beatSinWaveTrailBeat = Pattern.pattern('_beatSinWaveTrailBeat')(isolateCanvas(arg('weightedMeanWeight=0 +0.4 - 0.5*beat ')(addP(__beatInt4Hue(_beatSinwave),blur(weightedMean2P(black,trivial))))))

_beatWorm = Pattern.pattern('_beatWorm')(arg('''scaleTranslateX=frame/70.; scaleX= 0.5+(2*(abs(1-totalBeats%2)-0.5)*0.25) ''')(scaleAndTranslateCanvas(_beatSinwave)))
_starWars = Pattern.pattern('_starWars')(arg('scaleTranslateX=frame/23.; scaleX=0.97;generationSurviveRange=[3,4,5]; generationBornRange=[2]; generationStates=4; generationNeighborDistance=1')(scaleAndTranslateCanvas(_gameOfGenerations)))