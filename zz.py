# imports & arabtrans {{{

from browser import document as d
from browser import html as t
from browser import window as w
from browser import bind
from browser.local_storage import storage
from browser.timer import set_timeout, set_interval
import time

_arabtrans = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
def arabnum(n):
  return str(n).translate(_arabtrans)

# }}}

# darkmode, audio recitation (to-do), quiz mode (Enter vs TXT; to-do)
otherparams = '&zz&mv=r&d'

def update_otherparams():
  global otherparams
  otherparams = '&zz&mv=r'
  otherparams += '&d' if d['dark_chk'].checked else ''
  otherparams += '&c=n' if not d['taj_chk'].checked else ''


FIRST_TIME_INTERVAL = 6

# name, lengths, and rukus_of_sura {{{

names = [ 'الفاتحة', 'البقرة', 'آل&nbsp;عمران', 'النساء', 'المائدة', 'الأنعام', 'الأعراف', 'الأنفال', 'التوبة', 'يونس', 'هود', 'يوسف', 'الرعد', 'إبراهيم', 'الحجر', 'النحل', 'الإسراء', 'الكهف', 'مريم', 'طه', 'الأنبياء', 'الحج', 'المؤمنون', 'النور', 'الفرقان', 'الشعراء', 'النمل', 'القصص', 'العنكبوت', 'الروم', 'لقمان', 'السجدة', 'الأحزاب', 'سبأ', 'فاطر', 'يس', 'الصافات', 'ص', 'الزمر', 'غافر', 'فصلت', 'الشورى', 'الزخرف', 'الدخان', 'الجاثية', 'الأحقاف', 'محمد', 'الفتح', 'الحجرات', 'ق', 'الذاريات', 'الطور', 'النجم', 'القمر', 'الرحمن', 'الواقعة', 'الحديد', 'المجادلة', 'الحشر', 'الممتحنة', 'الصف', 'الجمعة', 'المنافقون', 'التغابن', 'الطلاق', 'التحريم', 'الملك', 'القلم', 'الحاقة', 'المعارج', 'نوح', 'الجن', 'المزمل', 'المدثر', 'القيامة', 'الإنسان', 'المرسلات', 'النبأ', 'النازعات', 'عبس', 'التكوير', 'الانفطار', 'المطففين', 'الانشقاق', 'البروج', 'الطارق', 'الأعلى', 'الغاشية', 'الفجر', 'البلد', 'الشمس', 'الليل', 'الضحى', 'الشرح', 'التين', 'العلق', 'القدر', 'البينة', 'الزلزلة', 'العاديات', 'القارعة', 'التكاثر', 'العصر', 'الهمزة', 'الفيل', 'قريش', 'الماعون', 'الكوثر', 'الكافرون', 'النصر', 'المسد', 'الإخلاص', 'الفلق', 'الناس' ]

# starting aya of rukus in suar
#_r = [[1],[1,8,21,30,40,47,60,62,72,83,87,97,104,113,122,130,142,148,153,164,168,177,183,189,197,211,217,222,229,232,236,243,249,254,258,261,267,274,282,284],[1,10,21,31,42,55,64,72,81,92,102,110,121,130,144,149,156,172,181,190],[1,11,15,23,26,34,43,51,60,71,77,88,92,97,101,105,113,116,127,135,142,153,163,172],[1,6,12,20,27,35,44,51,57,67,78,87,94,101,109,116],[1,11,21,31,42,51,56,61,71,83,91,95,101,111,122,130,141,145,151,155],[1,11,26,32,40,48,54,59,65,73,85,94,100,109,127,130,142,148,152,158,163,172,182,189],[1,11,20,29,38,45,49,59,65,70],[1,7,17,25,30,38,43,60,67,73,81,90,100,111,119,123],[1,11,21,31,41,54,61,71,83,93,104],[1,9,25,36,50,61,69,84,96,110],[1,7,21,30,36,43,50,58,69,80,94,105],[1,8,19,27,32,38],[1,7,13,22,28,35,42],[1,16,26,45,61,80],[1,10,22,26,35,41,51,61,66,71,77,84,90,101,111,120],[1,11,23,31,41,53,61,71,78,85,94,101],[1,13,18,23,32,45,50,54,60,71,83,102],[1,16,41,51,66,83],[1,25,55,77,90,105,116,129],[1,11,30,42,51,76,94],[1,11,23,26,34,39,49,58,65,73],[1,23,33,51,78,93],[1,11,21,27,35,41,51,58,62],[1,10,21,35,45,61],[1,10,34,53,70,105,123,141,160,176,192],[1,15,32,45,59,67,83],[1,14,22,29,43,51,61,76],[1,14,23,31,45,52,64],[1,11,20,28,41,54],[1,12,20],[1,12,23],[1,9,21,28,35,41,53,59,69],[1,10,22,31,37,46],[1,8,15,27,38],[1,13,33,51,68],[1,22,75,114,139],[1,15,27,41,65],[1,10,22,32,42,53,64,71],[1,10,21,28,38,51,61,69,79],[1,9,19,26,33,45],[1,10,20,30,44],[1,16,26,36,46,57,68],[1,30,43],[1,12,22,27],[1,11,21,27],[1,12,20,29],[1,11,18,27],[1,11],[1,16,30],[1,24,47],[1,29],[1,26,33],[1,23,41],[1,26,46],[1,39,75],[1,11,20,26],[1,7,14],[1,11,18],[1,7],[1,10],[1,9],[1,9],[1,11],[1,8],[1,8],[1,15],[1,34],[1,38],[1,36],[1,21],[1,20],[1,20],[1,32],[1,31],[1,23],[1,41],[1,31],[1,27],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]];

_r = [[1],[1,6,8,14,17,21,23,26,28,30,35,40,47,53,57,60,62,67,72,75,80,83,87,89,91,94,97,101,104,107,110,113,116,119,124,127,130,135,139,142,144,148,153,158,161,164,168,172,174,177,180,183,186,188,190,195,197,199,203,208,211,214,216,218,222,226,229,232,234,236,238,243,247,249,252,254,258,261,267,271,274,281,283,284],[1,5,7,10,14,18,21,26,28,31,33,35,38,42,45,47,51,55,58,64,67,72,76,79,81,83,86,92,96,98,102,104,110,113,116,121,130,137,144,146,149,152,154,156,159,162,165,169,172,176,179,181,185,187,190,194,196],[1,5,10,13,17,22,26,31,34,39,43,47,51,56,60,64,71,75,77,79,82,85,88,92,97,101,105,113,116,123,127,131,135,142,148,153,158,163,167,171,174],[1,3,5,7,10,12,14,17,20,23,27,31,35,40,43,47,51,54,57,61,65,67,70,74,78,82,87,90,94,96,101,105,109,112,116],[1,6,11,14,19,21,27,31,33,36,42,46,51,53,56,59,63,68,71,74,80,83,88,91,93,95,99,102,108,111,114,118,122,125,128,130,136,138,141,143,145,148,151,153,157,159,161],[1,6,11,13,19,22,26,28,32,35,38,40,44,48,52,54,59,65,70,73,75,80,85,88,94,100,103,109,117,127,130,134,138,142,145,148,152,156,158,161,163,166,169,172,175,179,182,186,189,194,199,203],[1,5,9,12,15,18,20,24,26,30,32,36,38,41,43,45,47,49,53,55,59,62,65,67,70,72,74],[1,4,7,12,17,19,23,25,28,30,34,36,38,40,43,49,54,60,64,67,71,73,75,81,86,90,94,97,100,103,107,111,113,117,119,123,128],[1,3,6,11,14,17,21,25,28,31,34,37,41,47,50,54,57,60,62,66,68,71,74,79,83,87,90,93,96,99,104,107],[1,4,6,9,12,15,18,21,25,29,32,36,41,44,47,50,53,58,61,63,66,69,72,77,81,84,87,90,93,96,100,105,110,114,118],[1,4,7,11,16,19,21,23,26,30,32,36,38,41,43,46,50,53,58,63,66,69,73,77,80,83,86,88,91,94,99,101,105,109],[1,3,5,8,12,15,16,17,19,23,27,30,32,35,38,41],[1,4,7,9,11,13,18,21,22,24,28,32,35,38,42,47],[1,6,16,21,26,30,36,45,51,61,72,80,87,94],[5,10,14,18,22,26,30,33,35,37,41,45,51,57,61,63,66,70,74,77,80,84,88,90,93,95,101,106,111,115,120,125],[1,4,7,11,15,18,23,26,31,34,37,40,45,48,53,56,58,61,66,70,73,78,81,85,89,94,97,101,105,110],[1,6,9,13,16,18,20,23,27,30,32,37,40,45,47,50,54,57,60,65,71,75,78,83,87,93,99,107],[1,7,12,16,22,27,31,35,41,46,51,58,61,66,73,77,83,88,96],[1,9,17,25,36,42,49,55,60,65,70,72,77,80,83,87,90,95,99,105,110,113,116,123,128,130,133],[1,5,11,16,19,25,30,36,42,45,48,51,56,62,71,74,78,83,87,92,97,101,104,108],[1,4,6,11,15,18,23,26,30,34,36,39,42,47,52,56,60,65,70,73,75],[1,12,17,23,25,31,38,45,51,57,62,68,73,78,84,91,99,105,112],[1,4,11,16,21,23,27,30,32,35,39,41,44,46,51,55,58,60,62],[1,4,7,10,17,21,25,32,35,41,45,51,56,61,67,72],[1,5,10,16,23,34,44,52,61,69,83,91,105,116,123,135,141,154,160,167,176,186,192,200,208,221],[1,7,10,15,18,20,23,27,32,38,41,45,49,54,59,63,67,72,79,83,87,89],[1,7,10,14,18,22,26,29,32,36,39,43,46,48,51,56,58,61,64,68,71,73,76,78,81,83,85],[1,8,10,14,19,24,28,31,36,40,45,48,52,56,61,64],[1,8,11,17,20,24,28,30,33,38,41,46,49,54,58],[1,8,12,14,16,20,22,25,28,31],[1,6,12,15,20,23,26],[1,4,6,9,12,16,18,21,25,28,31,35,37,38,41,49,51,53,54,56,59,63,69],[1,4,7,10,12,15,18,22,25,31,34,38,42,46,51],[1,4,8,10,12,15,19,27,31,36,38,40,42,44],[1,9,13,16,20,27,33,37,41,46,51,55,59,63,68,71,77,81],[1,12,22,33,40,50,62,75,83,91,99,103,114,123,133,139,149,158,167],[1,7,12,17,21,25,27,30,34,41,45,49,59,65,71,79],[1,5,7,10,14,19,22,24,32,36,39,42,47,49,53,56,60,64,70,73],[1,6,10,13,16,20,23,27,30,33,36,38,41,46,51,57,61,66,69,77,79,82],[1,6,9,13,15,19,23,26,29,33,36,39,42,45,49,52],[1,7,10,13,14,17,20,22,24,27,30,36,40,44,47,49,51],[1,9,15,20,24,31,36,40,46,51,57,63,68,74,81,85],[1,9,17,22,30,38,43,51],[1,7,12,16,18,22,24,27,30,33],[1,4,7,9,11,14,16,19,21,24,26,29,33],[1,3,7,12,14,16,20,25,29,35],[1,4,8,11,14,16,18,22,25,27],[1,4,8,11,12,14,16],[1,6,12,16,23,30,36,39],[1,15,24,31,38,47,52],[1,11,17,21,29,35,44],[1,10,19,26,31,33,43,50],[1,9,18,23,33,41,47],[1,17,26,33,46,60],[1,10,20,27,41,49,57,68,75,83,88],[1,4,7,9,11,13,16,18,20,22,25,27],[1,3,5,7,8,10,12,14,17,20],[1,3,6,7,9,11,13,15,18,22],[1,3,5,9,11],[1,5,7,10,13],[1,5,9],[1,5,9],[1,5,8,11,14],[1,2,4,6,8,11],[1,3,6,8,10],[1,5,12,18,23,27],[1,8,17,28,34,44],[1,9,19,25,38],[1,11,22,36],[1,5,10,16,21,26],[1,6,11,16,20,25],[1,11,19],[1,11,26,32,49],[1,16,31],[1,7,13,17,23,27],[1,20,29,41],[1,17,31,38],[1,15,27,34],[1,17,33],[1,15],[1,9],[1,7,14,22,29],[1,16],[1,10],[1],[1,9],[1,8,17],[1,15,21],[1,11],[1,11],[1,12],[1],[1],[1],[1,9],[1],[1,4,6],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]
# lengths of suar
lengths = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]

# indexes of rukus in suar: al-fatiha: [0], al-baqara: [1..40]
rukus_of_sura = []
for s in range(114):
  start = rukus_of_sura[-1][-1] + 1 if rukus_of_sura else 0
  count = len(_r[s])
  rukus_of_sura.append( list(range(start, start + count)) )

# }}}

# given sura_idx & ifrom (e.g., 1 & 8 for the third ruku in the Quran),
# return ruku_idx_of_sura (e.g., 1, for the third ruku in the Quran; [(0,0), (1,0), (1,1), ...])
def ruku_idx_of_sura(sura_idx, ifrom, *_):
  for ruku_idx, loop_ifrom in enumerate(_r[sura_idx]):
    if loop_ifrom == ifrom:
      return ruku_idx
  # TODO: improve & optimize, or eliminate

# encode and decode {{{

BAD_CHARS  = '[]/?@'
GOOD_CHARS = '()$!%'

BAD2GOOD = str.maketrans(BAD_CHARS, GOOD_CHARS)
GOOD2BAD = str.maketrans(GOOD_CHARS, BAD_CHARS)

BASE = 85

PAD_CHAR  = "'"
PAD_ORD   = ord(PAD_CHAR)
ZERO_ORD  = 42
ZERO_CHAR = chr(ZERO_ORD)

EF_MIN = 1.3
EF_MAX = 2.5
EF_SCALE = int(BASE**2 / (EF_MAX - EF_MIN))
# to represent EF by exactly 2 chars (no pad; len is known)

def encode_int(n, pad=True, length=0):
  if n != int(n) or n < 0:
    raise ValueError(f"encode_int takes only nonnegative integers; given: `{n}`")
  s = ''
  while n != 0:
    s = chr(n % BASE + ZERO_ORD) + s
    n //= BASE
  # if n == 0 and the loop didn't excute
  if s == '':  s = ZERO_CHAR
  # use fixed length (zeropadded)
  if length:   s = ZERO_CHAR * (length - len(s)) + s
  # padding to encode the length, b/c we don't use delimiters between values
  elif pad:    s = PAD_CHAR * (len(s) - 1) + s
  # sanitize "bad" characters
  s = s.translate(BAD2GOOD)
  return s

def decode_int(s):
  n = 0
  s = s.translate(GOOD2BAD)
  for c in s:
    if c == PAD_CHAR: continue
    n = n * BASE + ord(c) - ZERO_ORD 
  return n

def clamp_ef(ef):
  if ef < EF_MIN: ef = EF_MIN
  if ef > EF_MAX: ef = EF_MAX
  return ef

def fix_ef(ef): return int( (clamp_ef(ef) - EF_MIN) * EF_SCALE)
def defix_ef(ef): return ef / EF_SCALE + EF_MIN

def encode_ef(ef): return encode_int(fix_ef(ef), length=2)
def decode_ef(ef): return defix_ef(decode_int(ef))

# }}}
# time {{{

EPOCH = 1625616000

def ts2hr(ts):
  return round((time.mktime(ts) - EPOCH) / 3600)

def hr2ts(hr):
  return time.gmtime(hr * 3600 + EPOCH)  # TODO: or locattime?

def hr_now(): return ts2hr(time.localtime())

# }}}
# compute_rukuinfo {{{

class Mem:
  #
  def __init__(self, *a, **kw):
    self.set_parameters(*a, **kw)
  #
  def set_parameters(self, repitition=0, efactor=2.5, interval=0, lastreview=None):
    self.__repitition = int(repitition)
    self.__efactor    = clamp_ef(efactor)
    self.__interval   = round(interval)
    self.__lastreview = round(lastreview) if lastreview is not None else None
  #
  @property
  def repitition (self): return self.__repitition 
  @property
  def efactor    (self): return self.__efactor    
  @property
  def interval   (self): return self.__interval   
  @property
  def lastreview (self): return self.__lastreview 
  #
  # def __getitem__(self, idx=None):
  #   if idx != int(idx) or idx > 3 or idx:
  #     raise TypeError("indices must be integers")
  #
  def isdue(self, now=hr_now()):
    return self.lastreview is not None and now >= self.lastreview + self.interval
  #
  def serialize_parameters(self, epoch=0):
    if not self.ismemoed():
      return ''
    return (
        encode_int(self.repitition) +
        encode_ef(self.efactor)     +
        encode_int(self.interval)   +
        encode_int(self.lastreview - epoch)
      )
  #
  @efactor.setter
  def efactor(self, efactor):
    self.__efactor = clamp_ef(efactor)
  #
  def ismemoed(self):
    return self.lastreview is not None
  #
  def update_parameters(self, grade):
    if grade < 3:  # if wrong
      self.__repitition = 0
      self.__interval   = 0
    elif not self.ismemoed() or self.repitition == 0:  # if first time
      self.__repitition = 1
      self.__interval   = FIRST_TIME_INTERVAL
    elif self.isdue():  # if reviewing
      self.__repitition += 1
      self.__interval = round(self.interval * self.efactor)
    else:
      # do nothing (just update lastreview; as others)
      pass
    #
    self.__lastreview = hr_now()
    grade_complment = 5 - grade
    self.efactor += 0.1 - grade_complement * (0.08 + grade_complement * 0.02)

class Card(Mem):
  #
  def __init__(self, sura_idx, ifrom, ito, ruku_abs_idx, ruku_sura_idx, *a, **kw):
    super().__init__(*a, **kw)
    self.__sura_idx      = int(sura_idx)
    self.__ifrom         = int(ifrom)
    self.__ito           = int(ito)
    self.__ruku_abs_idx  = int(ruku_abs_idx)
    self.__ruku_sura_idx = int(ruku_sura_idx)
  #
  @property
  def ifrom(self):          return self.__ifrom
  @property
  def ito(self):            return self.__ito
  @property
  def afrom(self):          return arabnum(self.__ifrom)
  @property
  def ato(self):            return arabnum(self.__ito)
  @property
  def sura_idx(self):       return self.__sura_idx
  @property
  def sura_num(self):       return self.__sura_idx + 1
  @property
  def sura_name(self):      return names[self.__sura_idx]
  @property
  def ruku_abs_idx(self):   return self.__ruku_abs_idx
  @property
  def ruku_sura_idx(self):  return self.__ruku_sura_idx
  @property
  def ruku_num(self):       return self.__ruku_sura_idx + 1

# for each ruku: sura number, in-sura start aya, and in-sura end aya plus one
# making rukus overlap inside suar
# also save SM-2 factors: n (repitition number), ef (EF), hr (hours until next review)
def compute_rukuinfo():
  rukuinfo = []; i = 0
  for s in range(114):
    for k in range(len(_r[s])):
      ifrom       = _r[s][k]
      try:    ito = _r[s][k+1]
      except: ito = lengths[s]
      rukuinfo.append(Card(s, ifrom, ito, i, k)); i += 1
      # n, ef, hr, lr = 0, 2.5, 0, None  # the defaults
      # rukuinfo.append( { 'idx':(s, ifrom, ito), 'n':n, 'ef':ef, 'hr':hr, 'lr':lr } )
  return rukuinfo

# }}}
# rukuinfo, serialize, and deserialize {{{

def serialize(rukuinfo):
  serial = 'ZZX' + encode_int(0)
  try:
    epoch = min(r.lastreview for r in rukuinfo if r.lastreview is not None)
  except ValueError:  # mostly likely: min() arg is an empty sequence
    return ''
  serial += encode_int(epoch, pad=False) + PAD_CHAR
  #
  for sura_idx in range(114):
    (rr, rukuinfo) = (
        [ r for r in rukuinfo if r.sura_idx == sura_idx ],
        [ r for r in rukuinfo if r.sura_idx != sura_idx ])
    rr = [ r for r in rr if r.lastreview is not None ]
    if len(rr) == 0: continue
    serial += encode_int(sura_idx + 1)
    #
    if len(rukus_of_sura[sura_idx]) == 1:
      serial += rr[0].serialize_parameters(epoch)
    else:
      for r in rr:
        ruku_num = encode_int(ruku_idx_of_sura(r.sura_idx, r.ifrom) + 1)
        serial += ruku_num + r.serialize_parameters(epoch)
      serial += ZERO_CHAR
  #
  return serial

def deserialize(serial):
  #
  def tokenize():
    nonlocal serial
    i = 0
    for i in range(len(serial)):
      if serial[i] != PAD_CHAR: break
    ii = 2*i+1
    (tok, serial) = serial[:ii], serial[ii:]
    return tok
  #
  def read_int(): return decode_int(tokenize())
  def read_idx(): return decode_int(tokenize()) - 1
  def read_ef():  return decode_ef(tokenize() + tokenize())
  def read_lr():  return decode_int(tokenize()) + epoch
  #
  if serial == '': return
  print(serial)
  rukuinfo = compute_rukuinfo()
  if serial[:3] != 'ZZX':
    return  # error
  else:
    serial = serial[3:]
  version = read_int()
  (epoch, serial) = serial.split(PAD_CHAR, 1)
  epoch = decode_int(epoch)
  #
  while serial:
    sura_idx = read_idx()
    # print('S:', sura_idx+1)
    if len(rukus_of_sura[sura_idx]) == 1:
      s = serial; print(names[sura_idx], '-', read_int(), f'{read_ef():g}', read_int(), read_lr() ); serial = s
      rukuinfo[rukus_of_sura[sura_idx][0]].set_parameters(
        read_int(), read_ef(), read_int(), read_lr() )
    else:
      while (ruku_idx := read_idx()) != -1:
        s = serial; print(names[sura_idx], ruku_idx, read_int(), f'{read_ef():g}', read_int(), read_lr() ); serial = s
        rukuinfo[rukus_of_sura[sura_idx][ruku_idx]].set_parameters(
          read_int(), read_ef(), read_int(), read_lr() )
  #
  return rukuinfo

def show_info(r=None):
  if r is None:
    r = int(d['msg'].dataset['r'])
  d['info'].html = arabnum(f"""
      {rukuinfo[r].sura_name}    &emsp;
      {rukuinfo[r].ruku_num}
     ({rukuinfo[r].ifrom})       &emsp;
      {rukuinfo[r].repitition}   &emsp;
      {rukuinfo[r].efactor:g}    &emsp;
      {rukuinfo[r].interval}     &emsp;
      {rukuinfo[r].lastreview}   &emsp;
    """)

@bind(w, 'contextmenu')
def xyzzzzz(ev):
  if ev.target.tagName != 'A':  # b/c #msg has data-r, too
    return True  # do nothing; ie, let the menu be invoked
  try:
    r = int(ev.target.dataset['r'])
  except:  # not on a card
    return True  # do nothing; ie, let the menu be invoked
  show_info(r)
  return False  # override the context menu
  

def save_rukuinfo(rukuinfo):
  storage['rukuinfo'] = serialize(rukuinfo)

def load_rukuinfo():
  try:
    return deserialize(storage['rukuinfo'])
  except KeyError:
    return None

rukuinfo = load_rukuinfo() or compute_rukuinfo()

# }}}

def nowcards(s):
  now = hr_now()
  return [ r for r in rukus_of_sura[s] if rukuinfo[r].isdue(now) ]

def cards_html(onlynowcards=False):
  if onlynowcards:
    return "".join(fmt_sura(s, nowcards(s)) for s in range(114))
  else:
    return "".join(fmt_sura(s, rukus_of_sura[s]) for s in range(114))

# cards functions {{{

def show_pop(_=0):
  d['pop'].hidden = False
  d['pop'].style.opacity = 100
  d.body.class_name = 'scrolllock'

def hide_pop(_=0):
  d.body.class_name = ''
  d['pop'].style.opacity = 0
  def _real_hide():
    d['pop'].hidden = True
  set_timeout(_real_hide, 500)
  show_info()

def recite_btn(ev):
  r = int(ev.target.dataset['r'])
  card = rukuinfo[r]
  #
  d['msg'].html = "كيف حال حفظك للآيات من&nbsp;{} إلى&nbsp;{} من&nbsp;سورة&nbsp;{}؟"\
      .format(card.afrom, card.ato, card.sura_name)
  d['msg'].dataset['r'] = r
  d.body.class_name = 'scrolllock'
  return True  # to still load the href

def update_cards():
  d['allcards'].html = cards_html(onlynowcards=False)
  #
  nowcards = cards_html(onlynowcards=True)
  d['nowcards'].html = nowcards
  d['now'].hidden = nowcards == ''
  #
  for a in d.select('a[data-r]'):  # all cards; see fmt_cell()
    a.bind('click', recite_btn)
  #
  # DEBUG:
  # deserialize( serialize( rukuinfo ) )

# }}}

def url_for_card(r):
  card = rukuinfo[r]
  s = card.sura_num
  return f"?{s}/{card.ifrom}-{s}/{card.ito}{otherparams}"

def update_href_params():
  update_otherparams()
  for a in d.select('a[data-r]'):
    a.href = url_for_card(int(a.dataset['r']))

# formatting and onload {{{

def fmt_cell(r):
  card = rukuinfo[r]
  color = f' class="ef{round(card.efactor * 10)}"' if card.ismemoed() else ''
  #
  return f"""<a role="button" data-r="{r}" {color}
             title="تسميع سورة {card.sura_name} من الآية {card.afrom} إلى الآية {card.ato}"
             href="{url_for_card(r)}">{card.afrom}</a>"""

def fmt_sura(s, rukus):
  cards = "".join(fmt_cell(r) for r in rukus)
  label = arabnum(s+1) + " " + names[s] + ":"
  return f"<div><span>{label}</span><span>{cards}</span></div>\n" if cards else ""

def onload():
  # add cards
  update_otherparams()  # reloading keeps the checkboxes' values
  update_cards()
  set_interval(update_cards, 5*60*1000)  # every 5 minutes
  #
  # functionalize the import and export buttons
  @bind(d['export'], 'click')
  def export(ev=0):  # https://stackoverflow.com/q/3665115
    filename = time.strftime('Export-%Y-%m-%d-%H%M.ZZX')
    # blob = w.Blob.new(serialize(rukuinfo), {'type':)
    # a = t.A(href=w.URL.createObjectURL(serialize(rukuinfo)), download='export.zz')
    a = t.A(href='data:application/octet-stream,' + serialize(rukuinfo), download=filename)
    d.body.appendChild(a)
    a.click()
    d.body.removeChild(a)
  #
  @bind(d['import'], 'click')
  def import_(ev):
    file = t.INPUT(Id='infile', Type='file')
    # https://www.geeksforgeeks.org/how-to-read-a-local-text-file-using-javascript/
    @bind(file, 'change')
    def read(ev):
      reader = w.FileReader.new()
      @bind(reader, 'load')
      def red(e):
        global rukuinfo
        rukuinfo = deserialize(reader.result)
        update_cards()
        save_rukuinfo(rukuinfo)
      reader.readAsText(file.files[0])
    file.click()
  #
  # functionalize the grading buttons 
  #
  d['dismiss'].bind('click', hide_pop)
  #
  def set_ef(r, q):
    rukuinfo[r].update_parameters(q)
    update_cards()
    save_rukuinfo(rukuinfo)
    hide_pop()
  #
  for i in range(6):
    d[f'q{i}'].bind('click', lambda e, i=i: set_ef(int(d['msg'].dataset['r']), i))
  #
  # functionalize the dark & color buttons
  #
  @bind(d['dark_btn'], 'click')
  def __dark_btn_click(ev):
    d['dark_chk'].checked ^= 1  # toggle
    update_href_params()
  #
  @bind(d['taj_btn'], 'click')
  def __taj_btn_click(ev):
    d['taj_chk'].checked ^= 1  # toggle
    update_href_params()

onload()

# }}}

def _hide_recite():
  d['recite'].hidden = True
  d['recite'].src = 'about:blank'

def zz_ignore():
  _hide_recite()
  d.body.class_name = ''
w.zz_ignore = zz_ignore

def zz_done():
  _hide_recite()
  show_pop()
w.zz_done = zz_done

def zz_show():
  d['recite'].hidden = False
  d['recite'].focus()
w.zz_show = zz_show

# vim: set foldmethod=marker foldmarker={{{,}}} :
