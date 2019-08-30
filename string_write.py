#one large method to iterate through string and output updated string 
import random

def writeString( word, rules, depth ):

    #rules = [ [%,word,rule], [%,word,rule], [%,word,rule] ]
    if depth == 0:
        return word
    
    else:
        # iterate through word, find if any rules apply
        # where rule applies, add in result, must calculate percentages
        # where doesn't apply, just add the existing letter
        # recurse 

        temp = ""

        for item in word:
            
            rulesToApply = []

            # finds which rules must be applied 
            for i in range( len(rules) ):
            
                if item == rules[i][1]:
                    rulesToApply.append( rules[i] )
            
            # no rules apply
            if len(rulesToApply) == 0:
                temp += item
            
            # one rule applies
            elif len(rulesToApply) == 1:
                temp += rulesToApply[0][2]

            # multiple rules apply
            else:
                # SORT RULESTOAPPLY BY INCREASING % CHECK IF WORKS??

                for i in range( len(rulesToApply)-1 ): 
                    for j in range( 1,len(rulesToApply) ):
                        
                        if rulesToApply[i][0] < rulesToApply[j][0]:
                            tempRule = rulesToApply[i][0]
                            rulesToApply[i][0] = rulesToApply[j][0]
                            rulesToApply[j][0] = tempRule


                
                # finds rule to use by random number
                selector = random.randint(1,101)
                cuttoff = 0

                for i in range( len(rulesToApply) ):
                    
                    cuttoff += rulesToApply[i][0]
                    if selector <= cuttoff:
                        break

                temp += rulesToApply[i][2]

        return writeString( temp, rules, depth-1 )

#print writeString( 'F', [[100, 'F','[-FL]F[F[-FB-&&>F][&>F]]']],3 )
