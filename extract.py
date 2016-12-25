#这部分是读取切词的结果生成关键词与答案类型，输入输出文件名都已经写在代码中
import csv
noUsewords=['了','《','》','‘','’','“','”','，','？']
stopWords=['的','是','什么','第几','过','一共','多少','只','分别','年']
criticalQuality=['n','nrt','ns','nr','nz','nt','m','nd','nh','ni','l','i','t','spe']
noun=['n','ns','nz']
peoplewords=['者','人','家','男性','女性','代表']
placewords=['国籍','国家','大洲','大洋','山','地区','地点','县','市','省']
def parseResult(l):
    l=l.strip().split(',')
    quality=[]
    words=[]
    for i in range(len(l)):
        part=l[i]
        if not part:
            continue    
        part=part.split(' ')
        j=0
        if not part[j]:
            j+=1
        if part[j] not in noUsewords:
            if part[j]:
                words.append(part[j])
                quality.append(part[j+1])    
    return words,quality
def doExtract(words,quality):
    People=False
    Number=False
    Place=False
    Time=False
    index=0
    for word in words:
        if word=='谁' or word=='哪位' or word=='名叫':
            People=True
        if (word.find('多少')!=-1 or word.find('几')!=-1) and (quality[index]=='m'):
            Number=True
        if word=='位于' or word=='哪里':
            Place=True
        if word=="何时" or word=="哪年" or word=="哪一年":
            Time=True 
        index+=1           
    criticalWords=[]
    for i in range(len(words)):
        if quality[i] in criticalQuality and words[i] not in stopWords and words[i][0]!='一' and words[i][0]!='几':
            #print(words[i])
            if words[i][0]!='多':
                criticalWords.append(words[i])                    
    #已经获得了用于搜索的关键词列表 print(criticalWords)
            
    if People:
        return 'People',criticalWords
    if Number:
        return 'Number',criticalWords
    if Place:
        return 'Place',criticalWords
    if Time:
        return 'Time',criticalWords
    end = len(words)-1    
    index=len(words)-1
    Type='NO'
    while index>=1:
        if words[index]=='什么':
            tempindex = index
            while tempindex<end:
                if quality[tempindex+1] in noun:
                    Type=words[tempindex+1]
                    break
                tempindex+=1
            if Type!="NO":
                break                
            if words[index-1]=='是':
                index=index-1
            if index>=1:
                if quality[index-1] in noun:
                    Type=words[index-1]
                    break
        if words[index].find('哪')!=-1:#=='哪一' or words[index]=='哪个' or words[index]=='哪种' or words[index]=='哪部' or words[index]=='哪些':
            tempindex = index
            while tempindex<end:
                if quality[tempindex+1] in noun:
                    Type=words[tempindex+1]
                    break 
                tempindex+=1
            if Type !="NO":
                break                   
        if words[index]=='是':
            if index>=1:
                if quality[index-1] in noun:
                    Type=words[index-1]
                    break
        index=index-1  
    if Type=='NO':
        index=0
        while index<end:
            if words[index]=='哪':
                tempindex=index+1
                while tempindex<=end:
                    if quality[tempindex] in noun:
                        Type=words[tempindex]
                        break
                    tempindex+=1    
                if Type!='NO':
                    break
            index+=1
    if Type in  peoplewords:
        return 'People',criticalWords
    if Type in placewords:
        return 'Place',criticalWords
    if Type.find('书')>=0:
        return 'Book',criticalWords
    return Type,criticalWords
                                          