#encoding:utf-8
'''
Created on 2016��9��8��

@author: liuyu
'''


def generateSourcefile(glossaryfile, xiepeiyidic):
    with open(glossaryfile, 'rt', encoding='utf-8') as greader, open(xiepeiyidic, 'rt', encoding='utf-8') as xreader, open(sourcefile, 'wt', encoding='utf-8') as writer:
        glines = greader.readlines()
        xlines = xreader.readlines()
        for gl in glines:
            gl = gl.split()
            pos = gl[1]
            gl = gl[0]
            if pos == 'V':
                for xl in xlines:
                    writer.write(gl+'\t'+xl)
                

if '__main__' == __name__:
    glossaryfile = './hownet/glossary.dat'
    xiepeiyidic = './result/bt_xiepeiyiVerb.dic'
    sourcefile = './result/im_sourcefile.dat'
    
    
    generateSourcefile(glossaryfile,xiepeiyidic,sourcefile)
    
    
        
