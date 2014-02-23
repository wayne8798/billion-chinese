import webbrowser
import os
import random

def displayCallback(url,dict):
    f = open('data.js','w')
    f.write( 'var wordDict = {imgsrc: "' + url + '", dict:[')
    first = 1;
    for (k,v) in dict.items():
        if first == 1:
            first = 0
        else:
            f.write( ',')    
        f.write( '{text:"'+k+'", weight:'+str(v)+'}')
    f.write( ']};')
    f.close()
    webbrowser.open_new("file://"+os.getcwd() + "/WordCloud.html");




s = 'Lorem ipsum dolor sit amet, habeo elaboraret neglegentur ad sit, id cum omittam oporteat. Recteque partiendo imperdiet pro et, pri id minimum partiendo delicatissimi. Aperiri nusquam id quo, ea falli ullamcorper duo. At laboramus consequuntur pri. Mazim dicit commune pro no, cu est dico numquam deserunt. Vix utinam soleat scriptorem cu.'
a = s.split(' ')
d = dict()
for w in a:
    d[w]= random.randint(0,10);
url='http://static.freepik.com/free-photo/free-cube-design-background_52-10020.jpg'

displayCallback(url,d)

