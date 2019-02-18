# Locality Hashing

This repo contains two approaches to finding similarities within a set of questions.<br>
Amazon's Jaccard similarity algorithm is used.<br>

nativeJaccard is a naive loop through all elements (complete, but unreasonable for large datasets).<br>
localityHashing uses locality sensitive minhashing to exponentially speed up the process.

The sample question file is tab separated and formatted like so:
    
    qid     question
    1	What is the story of Kohinoor (Koh-i-Noor) Diamond?
    5	How can I increase the speed of my internet connection while using a VPN?
    7	Why am I mentally very lonely? How can I solve it?
    9	Which one dissolve in water quikly sugar, salt, methane and carbon di oxide?
    11	Astrology: I am a Capricorn Sun Cap moon and cap rising...what does that say about me?
    13	Should I buy tiago?
    15	How can I be a good geologist?
    17	When do you use シ instead of し?
    19	Motorola (company): Can I hack my Charter Motorolla DCX3400?
    21	Method to find separation of slits using fresnel biprism?
    23	How do I read and find my YouTube comments?
	
When tested on a database of 300k questions, localityHashing processed and outputted the similar qid's
in under 7 minutes consistently, while nativeJaccard took many hours.