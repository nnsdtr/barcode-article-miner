import sys
import codecs
import time
import glob
import os
import re

# Vocabulary:
#  ABS:   Abstract section related title
#  KEY:   Keywords section related title
#  INT:   Introduction section related title
#  MAME:  Materials and Methods section related title
#  RES:   Results section related title
#  DISC:  Discussion section related title
#  CONC:  Conclusion section related title
#  ACKN:  Acknowlegdements section related title
#  PHY:   "phylogeny" related term
#  IDNT:  "identification" related term

# Open output and Write header:
output=open('miner-output.txt', 'w')
header_row=['Filename','PHY','IDNT','ITS','18S','28S','RPB1','RPB2','TUB','TEF1']
header='\t'.join(header_row)+"\n"
output.write(header)

# Check if parameter were or not used. If not, ask user for path:
try:
  path=sys.argv[1]
except IndexError:
  print("\n"+"-"*50)
  print("Remember that you can also use path as a\nparameter for the script. Example call:\n\nbarcode-article-miner.py /home/user/text_directory")
  print("-"*50+"\n")
  print("\nPlease, insert bellow the path to the directory where the articles text files are located:\n")
  path=input("Path: ")
print("\n")

# Declare variables for processing and output statistics:
total_num_txt = len(glob.glob1(path,"*.txt"))
filenumber=0
num_operable_articles=0
num_accepted_articles=0
start = time.time()

# Open all .txt files, one per time:
for filepath in glob.glob(os.path.join(path, '*.txt')):
  filenumber+=1
  filename = os.path.basename(filepath)
  filename = filename.replace('.txt','')

  print("Progress: "+str(round((filenumber/total_num_txt)*100,2))+"%", end="\r")

  with codecs.open(filepath, encoding= "utf-8", errors= "ignore") as handle:
    txt = handle.readlines()

  # Text pre-processing (we've changed some characters to "⋅" for better coding with regex):
  for k in range(0,len(txt)):
    txt[k]=txt[k].replace("\t","⋅")
    txt[k]=txt[k].replace(" ","⋅")
    txt[k]=txt[k].replace(" ","⋅")
    txt[k]=txt[k].replace(" ","⋅")
    txt[k]=txt[k].replace("ﬁ","fi")

  # Declare dictionaries for the detection of titles and terms on the text (-1 = absent title):
  title_dict={"ABS":-1,"KEY":-1,"INT":-1,"MAME":-1,"RES":-1,"DISC":-1,"CONC":-1,"ACKN":-1}
  term_detect_dict={'PHY':-1,'IDNT':-1,'ITS':-1,'18S':-1,'28S':-1,'RPB1':-1,'RPB2':-1,'TUB':-1,'TEF1':-1}

  ## SEARCH SECTION TITLES AND LOCATE THEIR LINE NUMBERS ##
  # Search Abstract related title:
  for i in range(0,len(txt)):
    abst1 = re.search('^[Aa][⋅][Bb][⋅][Ss][⋅][Tt][⋅][Rr][⋅][Aa][⋅][Cc][⋅][Tt][⋅]?[^s]', txt[i])
    abst2 = re.search('^((\u000C)?(\[)?(?!\()[⋅]{0,5}[Aa][Bb][Ss][Tt][Rr][Aa][Cc][Tt][^Ss])', txt[i])
    summ = re.search('^((\u000C)?[S][Uu][Mm][Mm][Aa][Rr][Yy]\.?[⋅]{0,2})$|^([S][Uu][Mm][Mm][Aa][Rr][Yy](\.)?[⋅]{1,3})(?![⋅]{0,2}of|[⋅]{0,2}for|[⋅]{0,2}statistics)', txt[i])
    if abst1 or abst2 or summ:
      title_dict["ABS"]=i
      break
    else:
      continue

  # Search Keywords related title:
  for i in range(0,len(txt)):
    key = re.search('^(\u000C)?(\[)?[⋅]{0,5}[Kk][Ee][Yy][⋅]?[Ww][Oo][Rr][Dd][Ss]?(:)?', txt[i])
    if key:
      title_dict["KEY"]=i
      break
    else:
      continue

  # Search Introduction related title:
  for i in range(0,len(txt)):
    intr = re.search('^(\u000C[⋅]{0,5}|\x00[⋅]{0,5}|[⋅]{2}|[⋅]{0,5}\d.[⋅]{1,5}|\d[⋅]{1,5}|[⋅]{0,5}\d.0[⋅]{1,5}|1\u2003\|⋅\u2003)?[I][nN][tT][rR][oO][dD][uU][cC][tT][iI][oO][nN](?!,|[⋅]{1,2}\w|\.)', txt[i])
    back = re.search('^(1\.⋅)?[B][Aa][Cc][Kk][Gg][Rr][Oo][Uu][Nn][Dd](?!:)$', txt[i])
    if intr or back:
      title_dict["INT"]=i
      break
    else:
      continue

  # Search Materials and Methods related title (MAME):
  for i in range(0,len(txt)): 
    withnumber = re.search('^(\u000C)?[⋅]{0,2}\d((\.\d\.)|\.\d|\.|\d|⋅\|⋅⋅|())[⋅]{0,2}(([M][Aa][Tt][Ee][Rr][Ii][Aa][Ll][Ss]?[⋅]{0,2}$)|([M][Aa][Tt][Ee][Rr][Ii][Aa][Ll][Ss]?[⋅]{0,2}([Aa][Nn][Dd]|[&]))[⋅]{0,2}[Mm][Ee][Tt][Hh][Oo][Dd][Ss][⋅]{0,1})$', txt[i])
    materials = re.search('^((\u000C[⋅]{0,5})?■?[⋅]?[Mm][Aa][Tt][Ee][Rr][Ii][Aa][Ll][Ss]?[⋅]{1,3}([Aa][Nn][Dd]|[&])[⋅]{1,3}([Mm][Ee][Tt][Hh][Oo][Dd][Ss]?([⋅]{1,3})?(?!\.\))$|[Mm][Ee][Tt][Hh][Oo][Dd][Oo][Ll][Oo][Gg][Yy]$))|(^Material⋅and⋅morphological⋅methods$)|(Materials⋅and⋅Methods:⋅\w)', txt[i])
    methods = re.search('^(\u000C[⋅]{0,5})?[Mm][Ee][Tt][Hh][Oo][Dd][Ss]?(⋅DETAILS)?$|^\d\.⋅Methods$|^Methodology$|^Molecular⋅analysis$|^Methods⋅and⋅Results$', txt[i])
    if withnumber or materials or methods:
      title_dict["MAME"]=i
      break
    else:
      continue

  # Search Results related title:
  for i in range(0,len(txt)):
    result = re.search('^[⋅]{0,4}((\u000C)|■|\d\d\d|\d|\d\.\d|\d\.|3⋅\|⋅⋅)?[⋅]{0,4}[Rr][Ee][Ss][Uu][Ll][Tt][Ss][⋅]{0,4}$', txt[i])
    res_disc = re.search('^[⋅]{0,4}(\u000C|■|\d\d\d|\d|\d\.\d|\d\.|3⋅\|⋅⋅)?[⋅]{0,4}[Rr][Ee][Ss][Uu][Ll][Tt][Ss]?[⋅]{0,4}([Aa][⋅]?[Nn][⋅]?[Dd]|[&])[⋅]{0,4}[Dd][Ii][Ss][Cc][Uu][Ss][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,4}$', txt[i])
    res_ph = re.search('^Results⋅of⋅phylogenetic⋅analyses$', txt[i])
    if result or res_disc or res_ph:
      title_dict["RES"]=i
      break
    else:
      continue

  # Search Discussion related title:
  for i in range(0,len(txt)): 
    disc = re.search('^(\u000C)?(⋅)?(■|\d\.\d\.|\d\.\d|\d\.|\d⋅\||\d)?[⋅]{0,5}[Dd][Ii][Ss][Cc][Uu][Ss][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,5}$', txt[i])
    disc2 = re.search('^(\u000C)?(⋅)?(■|\d\.\d\.|\d\.\d|\d\.|\d⋅\||\d)?[⋅]{0,5}[Dd][Ii][Ss][Cc][Uu][Ss][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,5}([Aa][Nn][Dd]|[&])[⋅]{0,5}[Cc][Oo][Nn][Cc][Ll][Uu][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,5}$', txt[i])
    disc3 = re.search('^(\u000C)?(⋅)?(■|\d\.\d\.|\d\.\d|\d\.|\d⋅\||\d)?[⋅]{0,5}[Dd][Ii][Ss][Cc][Uu][Ss][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,5}([Aa][Nn][Dd]|[&])[⋅]{0,5}[Ll][Ii][Tt][Ee][Rr][Aa][Tt][Uu][Rr][Ee][⋅]{0,5}[Rr][Ee][Vv][Ii][Ee][Ww][Ss]?[⋅]{0,5}$', txt[i])
    if disc or disc2 or disc3:
      title_dict["DISC"]=i
      break
    else:
      continue

  # Search Conclusion related title:
  for i in range(0,len(txt)): 
    conc = re.search('^(\u000C)?(⋅)?(■|\d\.\d\.|\d\.\d|\d\.|\d⋅\||\d)?[⋅]{0,5}[Cc][Oo][Nn][Cc][Ll][Uu][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,5}$', txt[i])
    conc2 = re.search('^(\u000C)?(⋅)?(■|\d\.\d\.|\d\.\d|\d\.|\d⋅\||\d)?[⋅]{0,5}[Cc][Oo][Nn][Cc][Ll][Uu][Ss][Ii][Oo][Nn][Ss]?[⋅]{0,5}([Aa][Nn][Dd]|[&])[⋅]{0,5}[Oo][Uu][Tt][Ll][Oo][Oo][Kk][Ss]?[⋅]{0,5}$', txt[i])
    if conc or conc2:
      title_dict["CONC"]=i
      break
    else:
      continue

  # Search Acknowledgements related title:
  for i in range(0,len(txt)): 
    ackn = re.search('^(\u000C)?(\d\.\d|\d\.|\d)?[⋅]{0,37}[Aa][Cc][Kk][Nn][Oo][Ww][Ll][Ee][Dd][Gg][Ee][Mm][Ee][Nn][Tt][Ss]?[⋅]{0,5}', txt[i])
    if ackn:
      title_dict["ACKN"]=i
      break
    else:
      continue
  ## END OF: SEARCH SECTION TITLES AND LOCATE THEIR LINE NUMBERS ##

  # Remove from dictionary keys with value -1 (absent title = -1):
  for key,value in title_dict.copy().items():
    if value == -1:
       del title_dict[key]

  # Sort keys by value (Order is important for the next processes):
  sorted_title_dict = sorted(title_dict, key=title_dict.__getitem__)

  # Filter out inoperable publications:
  filtrate = []
  if "MAME" in sorted_title_dict:             # MAME must be present
    if sorted_title_dict[-1] != 'MAME':       # MAME must not be the last, otherwise limits of the section can't be found.
      if 'INT' in sorted_title_dict:          
        for i in range(0,len(sorted_title_dict)):   # Find the order sequence between INT and MAME for the next process.
          if sorted_title_dict[i] == 'MAME':
            MAME = i
          elif sorted_title_dict[i] == 'INT':
            INT = i

        if (INT < MAME):                # We've seen a small number of cases (nearly 0%) where the Abstract section have MAME
          num_operable_articles+=1      # title, causing misidentification of actual MAME location. Thus, for practical purposes,
          filtrate = sorted_title_dict   # we've chosen to discard those cases. One way to detect them was to compare INT and MAME
                                        # locations. If MAME occurs before INT, then something's wrong and the case is discarded.

      else:                             # Other cases were safe for MAME section location.
        num_operable_articles+=1
        filtrate = sorted_title_dict


  # Search biomarker terms on MAME:
  if len(filtrate) > 0:
    for k in range(0,len(filtrate)):
      if k+1 == len(filtrate):           # Prevent IndexError on the process.
        break
      if filtrate[k] == "MAME":
        # Search terms on the limits of MAME section:
        for j in range(title_dict[filtrate[k]],title_dict[filtrate[k+1]]):
          ITS = re.search('[I][T][S](?!⋅primer)(?!⋅\d|\–\d|\d|\-\d|\–[DdAa]|\-[DdAaBbCc])', txt[j])
          ITS1 = re.search('[I][Tt][Ss][⋅\-\–\/]?[1](?![FfTtLlKk]|\-[FfTtLlKk]|\d|[Hh])', txt[j])
          ITS2 = re.search('[I][Tt][Ss][⋅\-\–\/]?[2](?!8[Ss]|\-[Kk][Ll]|δ|\d)', txt[j])
          _28S = re.search('[^Oo][2][8][Ss]|[^t][L][S][U][^m]|[Ll][Aa][Rr][Gg][Ee][⋅][Ss][Uu][Bb][Uu][Nn][Ii][Tt]', txt[j])
          _18S = re.search('[^\dKkDd][1][8][Ss](\))?(⋅fungal|[⋅]{0,3}rRNA|[⋅]{0,3}rDNA)?(?![Vv][Dd][FfRr]|⋅[Vv][Dd][FfR]|\.|3|a|b|c|d|e|[Ff]|[⋅][Ff]|[Rr]|[⋅][R]|\-RP|UBR)', txt[j])
          SSU = re.search('((?<![Mm][Tt])(?<![Mm][Tt]⋅)(?<![Mm][Tt]⋅⋅)(?<![Mm][Rr])(?<![Mm][Rr]⋅)(?<![Mm][Rr]⋅⋅)(?<!mitochondrial⋅)(?<!mitochondrial⋅⋅))[S][S][U](?!mt|[⋅]{0,3}mt|[⋅]{0,3}mito|\_|[\dA-Qa-qS-Zs-z]|\-\d)', txt[j])
          small = re.search('(?<![Mm][Tt]⋅)(?<![Mm][Rr]⋅)(?<!mitochondrial⋅)[Ss][Mm][Aa][Ll][Ll][⋅-][Ss][Uu][Bb][Uu][Nn][Ii][Tt]', txt[j])
          RPB = re.search('[Rr][Pp][Bb][⋅]?[^\d]', txt[j])
          RPB1 = re.search('(?<![FfCc])[Rr][Pp][Bb][⋅]?([1]|[Ii][^Ii])(?!\w|\-[AaCcFfBb\d])', txt[j])
          RPB2 = re.search('[Rr][Pp][Bb][⋅]?([2]|[Ii][Ii])(?!\w|\-[AaCcFfBb\d])', txt[j])
          BenA = re.search('[Bb][e][n][A]', txt[j])
          TUB_2 = re.search('(?<!\w)[Tt][Uu][Bb][⋅]?[2]?(?!\w)', txt[j])
          beta_tubulin = re.search('([Bb][Ee][Tt][Aa]|[Bb]|[β])[\-⋅][Tt][Uu][Bb][Uu][Ll][Ii][Nn]', txt[j])
          beta_tub = re.search('([Bb][Ee][Tt][Aa]|[Bb]|[β])[\-⋅][Tt][Uu][Bb]\b', txt[j])
          TEF1a = re.search('[Tt][Ee][Ff][-⋅]?[1](α|alpha|a |\-α|\-a⋅|\-alpha)?(?![Rr][Ee][Vv])', txt[j])
          EF1a = re.search('[^Tt][Ee][Ff][-⋅]?[1][-⋅\n]?(α|alpha|a*\b|a*\d|\-α|\-a⋅|\-alpha)(?![Rr][Ee][Vv])', txt[j])
          PHY = re.search('[Pp][Hh][Yy][Ll][Oo][Gg][Ee][Nn]', txt[j])
          IDNT = re.search('(?<![Uu][Nn])(?<![Mm][Ii][Ss])(?<![Ee][Vv])(?<![Rr][Ee][Ss])[Ii][Dd][Ee][Nn][Tt][Ii](?![Tt][Ii][Ee][Ss]|[Cc][Aa][Ll]|[Ff][Ii][EeZz][DdIi][UuEe])', txt[j])

          # If detection is successful, assign presence tag (1) to related key:
          if ITS or ITS1 or ITS2:
            term_detect_dict["ITS"]=1
          if _18S or SSU or small:
            term_detect_dict["18S"]=1
          if _28S:
            term_detect_dict["28S"]=1
          if RPB1:
            term_detect_dict["RPB1"]=1
          if RPB2:
            term_detect_dict["RPB2"]=1
          if TUB_2 or BenA or beta_tubulin or beta_tub:
            term_detect_dict["TUB"]=1
          if TEF1a or EF1a:
            term_detect_dict["TEF1"]=1
          if PHY:
            term_detect_dict["PHY"]=1
          if IDNT:
            term_detect_dict["IDNT"]=1

    # Remove from dictionary keys with value -1 (absence tag):
    for key,value in term_detect_dict.copy().items():
      if value == -1:
        del term_detect_dict[key]
    
  ## PREPARE OUTPUT ##
  # Only articles returning MAME and (PHY or IDNT) were accepted:
  if (('MAME' in filtrate) and ('PHY' in term_detect_dict)) or (('MAME' in filtrate) and ('IDNT' in term_detect_dict)):

    num_accepted_articles+=1      # For statistics.
    
    MAME = term_detect_dict
    PHY=IDNT=ITS=_18S=_28S=RPB1=RPB2=TUB=TEF1=0 # Absence tag (0)
    if 'PHY' in MAME:
      PHY = 1
    if 'IDNT' in MAME:
      IDNT = 1
    if 'ITS' in MAME:
      ITS = 1
    if '18S' in MAME:
      _18S = 1
    if '28S' in MAME:
      _28S = 1
    if 'RPB1' in MAME:
      RPB1 = 1
    if 'RPB2' in MAME:
      RPB2 = 1
    if 'TUB' in MAME:
      TUB = 1
    if 'TEF1' in MAME:
      TEF1 = 1

    output_list=[filename,str(PHY),str(IDNT),str(ITS),str(_18S),str(_28S),str(RPB1),str(RPB2),str(TUB),str(TEF1)]
    output_row="\t".join(output_list)
    output_row+="\n"
    print(output_row)
    output.write(output_row)

# Conclusion statistics:
end_ = time.time()
print("\n%.2f seconds elapsed" % round(end_ - start,2))

accuracy=round(100*num_operable_articles/filenumber,2)
accuracyMAME=round(100*num_accepted_articles/filenumber,2)

print("Number of operable publications: ", str(num_operable_articles),"/",str(filenumber),"=",accuracy,"%")
print("No. pub. returning 'PHY' or 'IDNT': ", str(num_accepted_articles), "/",str(filenumber),"=",accuracyMAME,"%\n")
