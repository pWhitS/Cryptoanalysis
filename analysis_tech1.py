import sys

p1 = "sconced pouch bogart lights coastal philip nonexplosive shriller outstripping underbidding nightshirts colly editorializer trembler unresistant resins anthrax polypus research parapets gratuitous corespondent pyrometer breveted psychoneurosis scoutings almightily endoscopes cyanosis kayaker hake william blunted incompressibility lacer cumquat aniline agileness academe obstacle toothpick nondistribution rebukes concertizes industrialist plenipotentiary swagmen kevils dredge ostensible atavistic p"
p2 = "revelation revering rightest impersonalize juliennes scientists reemphasizing propose crony bald pampering discharged lincoln authoresses interacted laked bedmaker intolerably beltlines warningly worldliness serologic bottom guessed hangup vitiates snaky polypous manifolding sweatshirt divisiveness decapitation musketry versers pizzas aperies reorganizes fender presentations thereuntil fly entrapped causewayed shaped freemasonry nudging efflorescence hydrated zazen exegeses fracas unprogressivel"
p3 = "boca ingestion financed indexer generalships boldfaces boughed tesla videotext expiation brasil kinglets duality rattlesnakes mailability valvelet whimperingly corralled stench fatal inapplicably uncourageous bubblers req jesse foetor bulgaria hueless pickwicks intrans gargles purgations subvarieties pettier caste decongestive replanned continual bribed pirog learning currier careers rustling swankily onetime prearranges stowage responder inwrapped coign concubines gyrus delta tripled sleetier m"
p4 = "allocated demonstration cocoanuts imprecisions mikado skewer ennobled cathect universalizes lucidity soldierly calor narthexes jiggling mutinousness relight mistook electra ogles chirk unsympathetic indorsed theomania gaper moths aerospace riboflavin sensorium teariest luckiest dither subparts purslane gloam dictatory conversed confides medullary fatsos barked yank chained changes magicians movables ravenousness dipsomaniac budded windjammers stayers dixie tepidities desexualization boodled dile"
p5 = "shellackers ballets unselfishly meditatively titaness highballed serenaders ramshorns bottlenecks clipsheet unscriptural empoisoned flocking kantians ostensibilities heigh hydrodynamics qualifier million unlading distributed crinkliest conte germ certifier weaklings nickeled watson cutis prenticed debauchery variously puccini burgess landfalls nonsecular manipulability easterlies encirclements nescient imperceptive dentally sudsers reediness polemical honeybun bedrock anklebones brothering narks"


plaintext = ""
ciphertext = raw_input("Enter Ciphertext pls: ")
print

cipherList = ciphertext.split(" ")

l1 = len(p1.split(" ")[0])
l2 = len(p2.split(" ")[0])
l3 = len(p3.split(" ")[0])
l4 = len(p4.split(" ")[0])
l5 = len(p5.split(" ")[0])

firstword = cipherList[0]
fwlen = len(firstword.split(","))

if fwlen == l1:
	plaintext = p1
elif fwlen == l2:
	plaintext = p2
elif fwlen == l3:
	plaintext = p3
elif fwlen == l4:
	plaintext = p4
elif fwlen == l5:
	plaintext = p5

print "My plaintext guess: " + plaintext
print

