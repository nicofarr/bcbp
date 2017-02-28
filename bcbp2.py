## Author : Hamish Allan, 2007 - 2014 

import sys
import gc
import probstat
import random
from utils import PriorityQueue
from sets import Set

def triad_perms(triad):
    return [''.join(x) for x in probstat.Permutation([c for c in triad])]

def group_distrib(group):
    distrib = []
    for triad in group:
        for i in range(3):
            c = triad[i]
            o = ord(c) - 65
            while len(distrib) <= o:
                distrib.append([0, 0, 0])
            distrib[o][i] = distrib[o][i] + 1
    return distrib

def group_distrib_scores(group_distrib):
    return [max(x) - min(x) for x in group_distrib]

class GroupNode:
    def __init__(self, group):
        self.group = group
        self.distrib = group_distrib(group)
        self.score = sum(group_distrib_scores(self.distrib))

    def __str__(self):
        return group.__str__()

    def successors(self):
        succs = []

        for triad_index in range(len(self.group)):
            triad = self.group[triad_index]
            perms = triad_perms(triad)
            for perm_index in range(len(perms)):
                new_perm = perms[perm_index]
                if (new_perm != triad):
                    new_group = list(self.group)
                    new_group[triad_index] = new_perm
                    
                    new_node = GroupNode(new_group)
                    if (new_node.score < self.score):
                        succs.append(GroupNode(new_group))

        return succs

def random_perm(triad):
    return random.choice(triad_perms(triad))

def main():

    groups = [
              ['ABX', 'AFQ', 'ALR', 'BCD', 'GPV', 'BNQ', 'CEH', 'CJR', 'NUZ', 'DIZ', 'DOV', 'EHY', 'ENW', 'FHT', 'FOV', 'GJP', 'GSX', 'MSU', 'IKL', 'IPT', 'JKW', 'KQR', 'LSY', 'MUW', 'MOY', 'TXZ'],
              ['ABD', 'AFR', 'ALS', 'BCE', 'GPW', 'BNR', 'EIZ', 'CJS', 'CLT', 'DPY', 'DOW', 'HKZ', 'ENX', 'FHU', 'FOP', 'GJQ', 'GRY', 'HMV', 'IKM', 'ITW', 'JQX', 'KSZ', 'LNT', 'MUX', 'OVY', 'QUV'],
              ['ABW', 'AFS', 'ALT', 'BCF', 'GIP', 'BNS', 'CEJ', 'CJT', 'SUZ', 'DHV', 'OQX', 'ELZ', 'ENY', 'FHV', 'OPX', 'DGR', 'GRZ', 'HMW', 'DIK', 'ITX', 'JQY', 'KPQ', 'KLM', 'MUY', 'ORV', 'NUW'],
              ['ABV', 'AFT', 'ADY', 'CNY', 'BPY', 'BNT', 'CEK', 'CJU', 'PSV', 'DHW', 'DPR', 'LMV', 'ENZ', 'FHW', 'FLO', 'GJS', 'GIS', 'HMX', 'IKO', 'GIT', 'JQZ', 'KQU', 'ELR', 'MXZ', 'ORU', 'QWX'],
              ['ANT', 'AFM', 'ALV', 'BCP', 'BGZ', 'BNU', 'ELY', 'CJV', 'CSW', 'DHX', 'DOZ', 'EIN', 'EOP', 'FHX', 'FKQ', 'GJT', 'GSU', 'HMY', 'IKP', 'ITZ', 'JRS', 'KQV', 'LRW', 'DMW', 'ORX', 'QUY'],
              ['ABT', 'AEF', 'ALW', 'BCI', 'BIK', 'NSZ', 'CEM', 'CJW', 'NSX', 'DGY', 'DPQ', 'EHO', 'LOV', 'FHY', 'FPT', 'GJU', 'GPS', 'HMZ', 'KNQ', 'IUV', 'JRT', 'DKW', 'LRX', 'MVX', 'ORY', 'QUZ'],
              ['ABI', 'AFW', 'ALQ', 'KTX', 'BHJ', 'BNW', 'CEN', 'CSX', 'CSY', 'DMZ', 'DOP', 'EGP', 'ETU', 'FGZ', 'DFP', 'HJV', 'GLS', 'HNO', 'IKR', 'IUW', 'JRU', 'KQX', 'LRY', 'MVY', 'OTZ', 'MQV'],
              ['ABU', 'ADF', 'ALY', 'BKN', 'HKW', 'IMN', 'COV', 'CJY', 'CWZ', 'DIU', 'DPS', 'EHQ', 'EOT', 'FMT', 'FPS', 'GJW', 'GRX', 'HNP', 'BGL', 'IUX', 'JRV', 'KQY', 'LRZ', 'EMZ', 'OST', 'QVX'],
              ['ABK', 'AFG', 'ALZ', 'BCL', 'HMN', 'NUY', 'CEP', 'CJZ', 'HTU', 'DKV', 'DPT', 'EHR', 'EOR', 'FIW', 'FPV', 'GJX', 'DGS', 'NQX', 'IKT', 'BIY', 'JRW', 'OQZ', 'LMS', 'MWX', 'OSU', 'QVY'],
              ['ALU', 'AFP', 'ANW', 'CJM', 'BHM', 'BDN', 'CEQ', 'CKT', 'TVX', 'BLY', 'DUZ', 'EHS', 'DEO', 'FIO', 'FGP', 'GJY', 'GWX', 'HNR', 'IKU', 'IPZ', 'JRX', 'KRS', 'LSW', 'MYZ', 'OQV', 'QTV'],
              ['ABY', 'AGX', 'AMO', 'CLN', 'BHN', 'BOP', 'CER', 'CKU', 'QTW', 'DFY', 'DPV', 'DEH', 'EJX', 'FIM', 'FQY', 'GJZ', 'GTU', 'HNS', 'IKV', 'ILU', 'JPR', 'KRT', 'LSV', 'MWZ', 'OSW', 'QXZ'],
              ['ABN', 'AGZ', 'AMP', 'CLO', 'BHO', 'BDR', 'CES', 'CKM', 'QTX', 'DIN', 'DPW', 'EHU', 'EJQ', 'FIV', 'FPW', 'GLZ', 'GTV', 'HNT', 'IJK', 'VXY', 'JRZ', 'KRU', 'LSU', 'FMY', 'OSX', 'QWY'],
              ['ABR', 'AGJ', 'AMQ', 'BCU', 'BHP', 'DOR', 'CET', 'KNO', 'CTY', 'DIO', 'DPX', 'EHV', 'EJL', 'FNW', 'FPX', 'FGM', 'GTW', 'HNU', 'IKQ', 'IVY', 'JLS', 'KRV', 'LSX', 'MUZ', 'SYZ', 'QWZ'],
              ['ABP', 'AGW', 'AMR', 'CMQ', 'BHQ', 'BOY', 'CEU', 'DJV', 'CTX', 'DFT', 'DLN', 'EHW', 'EJO', 'FIP', 'FPU', 'GKN', 'GTX', 'HNV', 'IKY', 'IVZ', 'JSU', 'KRW', 'LRS', 'MSZ', 'LOZ', 'QXY'],
              ['ABQ', 'AGL', 'AMS', 'BCR', 'FHR', 'BOT', 'CEV', 'KMQ', 'TUW', 'DIY', 'DPZ', 'EHX', 'EUZ', 'FIQ', 'FPZ', 'GJO', 'GLT', 'HNW', 'DKY', 'CIY', 'JSV', 'KRX', 'LNS', 'NOP', 'MUV', 'JWX'],
              ['ABO', 'AGM', 'AMN', 'BSV', 'BHS', 'OPU', 'CEW', 'CKR', 'CUZ', 'DFX', 'DQR', 'EHJ', 'EPQ', 'FIX', 'DFR', 'GKP', 'GQZ', 'HNX', 'LMN', 'IWY', 'JSW', 'JKY', 'LTU', 'ILV', 'OTV', 'TYZ'],
              ['ADL', 'AGN', 'AMU', 'BJP', 'BHT', 'BHV', 'CEX', 'CFY', 'CUX', 'DGI', 'DJQ', 'EOZ', 'KPV', 'FIL', 'FQS', 'KQS', 'GUV', 'HNY', 'LNW', 'IWZ', 'JSX', 'KRZ', 'ETY', 'OPR', 'MOW', 'MRT'],
              ['ABG', 'AOX', 'AMV', 'BCH', 'BHU', 'DFW', 'CEY', 'CKL', 'PUY', 'DIP', 'DQZ', 'EJZ', 'EMP', 'FJV', 'FQT', 'GKR', 'GQW', 'HNZ', 'ILO', 'INX', 'JSY', 'KST', 'LMW', 'NRV', 'OTX', 'RSU'],
              ['ABJ', 'AGP', 'AMW', 'BCV', 'BOV', 'HLX', 'CEZ', 'CKN', 'NRZ', 'DJR', 'DQU', 'EFW', 'EPT', 'FIU', 'FQU', 'GKM', 'GXY', 'HPY', 'ILQ', 'IMZ', 'DJS', 'HKS', 'LWX', 'NOT', 'OTY', 'RSV'],
              ['AJN', 'AGQ', 'AMX', 'BCW', 'BEH', 'BMO', 'CFZ', 'KPS', 'CVW', 'DJX', 'DQV', 'LRV', 'EPU', 'FIN', 'FHQ', 'GKT', 'GUY', 'HOX', 'ILP', 'IYZ', 'JMT', 'EKS', 'LTY', 'NOU', 'DRZ', 'RSW'],
              ['AEM', 'AGR', 'AMY', 'BCG', 'BHX', 'BDZ', 'CFH', 'CPT', 'PXY', 'DIJ', 'DQW', 'EIM', 'EPV', 'FKN', 'FQW', 'KSU', 'GUZ', 'HOR', 'ILR', 'JLN', 'JTV', 'KSW', 'LTZ', 'NOQ', 'OUV', 'SXY'],
              ['ABC', 'AGS', 'ASW', 'CJN', 'BHY', 'PQU', 'CFI', 'LUX', 'PTY', 'DER', 'DQX', 'EHN', 'EPZ', 'FIR', 'FMQ', 'GKV', 'GVW', 'HOZ', 'ILZ', 'JKM', 'DJT', 'KMX', 'BLV', 'NOW', 'OTU', 'RSY'],
              ['ABM', 'AEG', 'ANR', 'HUW', 'BHZ', 'BPR', 'CFJ', 'CKS', 'CVZ', 'DIM', 'DNY', 'ELV', 'EPX', 'FIY', 'FPQ', 'GKW', 'GMV', 'HOT', 'ILT', 'JKN', 'JTX', 'QSY', 'LUW', 'DOX', 'OQU', 'RSZ'],
              ['ABZ', 'AGU', 'ANP', 'BDF', 'IJS', 'BJS', 'CFR', 'CHK', 'CWX', 'DHL', 'DQT', 'IPV', 'EPY', 'FIZ', 'EQZ', 'GKX', 'GVY', 'HOU', 'ELN', 'JKO', 'TWY', 'QSV', 'LMX', 'MNW', 'MOR', 'RTU'],
              ['ACD', 'AGV', 'ANQ', 'BDE', 'BHI', 'BRT', 'FLS', 'CLM', 'CYZ', 'JNU', 'RSX', 'EIQ', 'EPW', 'FJK', 'FRS', 'GKY', 'GQX', 'HOV', 'HIW', 'MPX', 'JWZ', 'KTU', 'DLY', 'MNO', 'OUZ', 'PTV'],
              ['AEK', 'ACH', 'ANO', 'BDG', 'BIL', 'BPU', 'CFM', 'CMY', 'HUZ', 'DMY', 'DST', 'EIR', 'EQR', 'FJY', 'FST', 'GKZ', 'GLX', 'HOP', 'IWX', 'JKQ', 'JUV', 'NVX', 'LSZ', 'NPQ', 'OVW', 'RTW'],
              ['ACT', 'AGH', 'ANS', 'DHQ', 'IPU', 'BPV', 'CFN', 'BNO', 'CXY', 'DKM', 'DRU', 'EIS', 'EQS', 'FJM', 'BEF', 'GTY', 'GLW', 'HOQ', 'ILX', 'KWZ', 'JUW', 'RTZ', 'JLV', 'KPZ', 'OVX', 'MRY'],
              ['ACQ', 'AGY', 'AHZ', 'BDW', 'IQT', 'BPW', 'CFO', 'LMP', 'BCM', 'DKS', 'DRV', 'EIU', 'EQT', 'FJN', 'FRV', 'GLN', 'GWZ', 'HOY', 'ELX', 'JKS', 'IJU', 'HKM', 'VXZ', 'NPS', 'OUY', 'RTX'],
              ['AHK', 'AGI', 'ANU', 'BDJ', 'BEM', 'BPX', 'CFP', 'CLQ', 'CWY', 'DJM', 'DRW', 'EIT', 'EQU', 'FJS', 'FRW', 'GMO', 'GXZ', 'HOS', 'ILS', 'HRV', 'NYZ', 'KUY', 'LVX', 'NPT', 'OVZ', 'KQT'],
              ['ACI', 'AHI', 'ANV', 'BDK', 'BIM', 'BGY', 'COQ', 'CLR', 'EFH', 'DTW', 'DRX', 'EOS', 'EQX', 'FJT', 'FXY', 'LNP', 'GSZ', 'HPQ', 'MNS', 'JKU', 'JUZ', 'KTW', 'LVZ', 'GPU', 'OWY', 'MRV'],
              ['ACJ', 'AHJ', 'AMT', 'BDS', 'BIN', 'CPZ', 'FKY', 'CLS', 'EGX', 'DLX', 'DRY', 'EIW', 'EOQ', 'FJQ', 'FHN', 'GMU', 'GYZ', 'HPR', 'IMO', 'BKV', 'PTU', 'KVW', 'LTX', 'NSV', 'OQW', 'RUZ'],
              ['ACK', 'AGK', 'ANX', 'BDM', 'BIR', 'BOQ', 'CFS', 'CST', 'EHT', 'DLV', 'ORZ', 'EIX', 'EQY', 'FJU', 'FHZ', 'GLR', 'GIJ', 'HPS', 'MPV', 'JQW', 'NTV', 'DKU', 'LWY', 'NPW', 'MOZ', 'UXY'],
              ['ACL', 'AHL', 'ANY', 'BNZ', 'IOS', 'BQS', 'CFT', 'CMU', 'DEG', 'JSZ', 'DRT', 'EGI', 'EQV', 'DFO', 'FRT', 'GMW', 'HIK', 'HPV', 'MQW', 'JKX', 'JVY', 'KPU', 'LWZ', 'NPX', 'BOX', 'RUY'],
              ['ACM', 'AHM', 'ANZ', 'BDO', 'BGT', 'BQT', 'GUX', 'CQV', 'DEJ', 'NVW', 'DOS', 'CEI', 'FQZ', 'FJP', 'FSW', 'GLU', 'HIL', 'HPT', 'IMR', 'KRY', 'EJV', 'KSY', 'KLX', 'NPY', 'OXZ', 'RUW'],
              ['ACN', 'AHN', 'AOQ', 'BDP', 'BIT', 'BQU', 'CFV', 'CLW', 'EKM', 'DJU', 'DSX', 'EGY', 'ERS', 'FOW', 'FVY', 'GLM', 'HIT', 'HJP', 'IMS', 'JKR', 'KUX', 'QTY', 'LXZ', 'NPZ', 'GOZ', 'RVW'],
              ['ACO', 'AHO', 'AOP', 'BDQ', 'BIS', 'BVX', 'CFW', 'CKX', 'DEL', 'KMT', 'DGW', 'EYZ', 'EGT', 'FIJ', 'FSU', 'GLV', 'HIN', 'HPU', 'MTZ', 'JMS', 'JUY', 'KNW', 'LYZ', 'NQR', 'PQR', 'RVX'],
              ['ACP', 'AHP', 'AOR', 'BKR', 'BGI', 'BTW', 'CFX', 'CLY', 'DEM', 'DGU', 'DSV', 'EJM', 'ERU', 'FJW', 'FSX', 'GWY', 'HIO', 'HPX', 'IMU', 'JKL', 'QYZ', 'KTV', 'NOZ', 'NQS', 'NQZ', 'LTV'],
              ['ACG', 'AHQ', 'AOS', 'BDL', 'BEX', 'BUX', 'CKY', 'CLZ', 'DEN', 'DIW', 'KUZ', 'JNW', 'ERV', 'FGX', 'FSY', 'FGU', 'HIP', 'HOW', 'IMT', 'JOS', 'JRY', 'KLV', 'MNP', 'MQT', 'PQT', 'RVZ'],
              ['ACR', 'AHR', 'AOT', 'BDT', 'IUY', 'BKQ', 'CFG', 'CMN', 'EOU', 'DLT', 'DSZ', 'EOV', 'ERW', 'FJL', 'FGS', 'GLY', 'HIQ', 'HPZ', 'IMW', 'JPY', 'JXZ', 'KVX', 'KMN', 'NSU', 'BPQ', 'VWX'],
              ['ACS', 'AHS', 'AOU', 'BDU', 'BIZ', 'BLQ', 'CGH', 'CMO', 'EFP', 'DJZ', 'DTU', 'EJP', 'ETX', 'FOZ', 'FTY', 'GKL', 'GIR', 'HKV', 'IMX', 'JLQ', 'NSY', 'KWX', 'MNR', 'NQV', 'PVW', 'RWY'],
              ['ACF', 'ATZ', 'AOV', 'BDV', 'BKW', 'BPS', 'CGJ', 'CMP', 'DEZ', 'DKX', 'RTV', 'EOX', 'EUY', 'FHL', 'FOT', 'GNU', 'HIS', 'HQS', 'IMY', 'JLR', 'LMU', 'KXY', 'GIN', 'NQW', 'JPQ', 'RWZ'],
              ['ACU', 'AHU', 'AVW', 'BGO', 'BSW', 'EKY', 'CGI', 'CQU', 'DIR', 'DJO', 'DJP', 'EJR', 'EFZ', 'FKM', 'FSV', 'GLO', 'HTY', 'HTW', 'IXZ', 'LPS', 'BLN', 'KVZ', 'MNT', 'MNQ', 'PQX', 'RXY'],
              ['ACV', 'AHV', 'AGO', 'BNX', 'BJM', 'BRU', 'CGP', 'CMR', 'DES', 'DKT', 'TVZ', 'EJS', 'ENS', 'FIK', 'FWX', 'GMP', 'HIU', 'HQU', 'INO', 'JLT', 'KLO', 'WYZ', 'FLW', 'DQY', 'PQY', 'RXZ'],
              ['ACW', 'AHW', 'AOY', 'BDI', 'BJN', 'BRV', 'CGL', 'CMS', 'DEF', 'GKO', 'DTY', 'EJT', 'ESU', 'FOX', 'FTU', 'GMQ', 'HIR', 'HQV', 'INP', 'JLU', 'KLP', 'KXZ', 'MNV', 'QSW', 'PXZ', 'RYZ'],
              ['AFX', 'AHX', 'AOZ', 'BCO', 'BJO', 'BIW', 'CGM', 'CMT', 'DEU', 'DKP', 'DTZ', 'EJU', 'ESV', 'FKP', 'FGH', 'GMR', 'IVW', 'HJQ', 'INQ', 'LVW', 'LQX', 'KYZ', 'LNY', 'NRS', 'PRS', 'TUY'],
              ['ACY', 'AHY', 'APQ', 'EFK', 'BCJ', 'BRX', 'BCS', 'LPU', 'DEW', 'DGK', 'DUV', 'JVZ', 'EGW', 'FOQ', 'FOU', 'GMS', 'HIX', 'HQX', 'INR', 'JLW', 'KOR', 'ILM', 'MNZ', 'NTY', 'PTZ', 'STV'],
              ['ACZ', 'ABH', 'APZ', 'EGZ', 'BJQ', 'BPT', 'CGO', 'CIV', 'DEV', 'DKR', 'DFU', 'EJW', 'QSX', 'FKR', 'FUW', 'MTY', 'HIY', 'GHX', 'INS', 'LQV', 'KLS', 'LMO', 'MNY', 'NOR', 'PUX', 'JTW'],
              ['ADE', 'AIJ', 'APV', 'BHW', 'BFR', 'BRZ', 'CGK', 'CMW', 'DEQ', 'DJK', 'GOU', 'OWX', 'ESY', 'FMS', 'FUX', 'GQU', 'HIZ', 'PQZ', 'INT', 'JLY', 'KLT', 'CHL', 'MNX', 'NOV', 'PRV', 'STY'],
              ['ACX', 'AIK', 'APT', 'IJO', 'BFJ', 'BST', 'CGQ', 'CMV', 'DEY', 'DVZ', 'DNO', 'EWY', 'ESZ', 'FHK', 'FUY', 'GVX', 'BHK', 'GHR', 'INU', 'JLZ', 'LQU', 'LMQ', 'MOP', 'NRW', 'PRW', 'STX'],
              ['ADG', 'ALO', 'APW', 'BFH', 'BJT', 'PQS', 'CGR', 'BCY', 'DEX', 'KUV', 'CDZ', 'EIJ', 'EIO', 'FKU', 'FUZ', 'GSW', 'HLY', 'HQT', 'INV', 'JMN', 'KVY', 'LMR', 'MOQ', 'NRX', 'PWX', 'STZ'],
              ['ADH', 'AIM', 'APS', 'BEK', 'BJU', 'BCX', 'CGS', 'CXZ', 'DFG', 'IQZ', 'DVW', 'EKL', 'ENT', 'FKV', 'FTW', 'GOX', 'HJM', 'HUY', 'INW', 'JMO', 'LQZ', 'LST', 'OQR', 'NRY', 'PRY', 'PUV'],
              ['ADI', 'AIN', 'APU', 'BEL', 'BJV', 'BSU', 'CGT', 'CNO', 'DFH', 'KQZ', 'GQV', 'DEK', 'ETW', 'FKW', 'FVX', 'GOY', 'HJN', 'HQR', 'IXY', 'JMP', 'LXY', 'LMT', 'MOS', 'CRZ', 'PRZ', 'SUW'],
              ['ADZ', 'AIO', 'APX', 'BEI', 'BJW', 'BSX', 'CUY', 'CNP', 'DFZ', 'DQS', 'QRW', 'EGK', 'EVX', 'CFK', 'FGV', 'GMZ', 'HJO', 'HRW', 'INY', 'JMQ', 'KLY', 'LRU', 'MOT', 'NST', 'LPT', 'HUV'],
              ['ADK', 'AIP', 'APY', 'BET', 'BLX', 'BSY', 'CGV', 'CQR', 'DFJ', 'GIQ', 'DTV', 'EOW', 'TVY', 'FKX', 'FWZ', 'GNO', 'HJZ', 'HRU', 'INZ', 'JMR', 'KLW', 'ELM', 'MOX', 'HNQ', 'PSU', 'CSU'],
              ['ALM', 'AIQ', 'APR', 'BEO', 'BJY', 'BSZ', 'CGW', 'CNR', 'DFK', 'IKN', 'HWX', 'DEP', 'ETZ', 'FKZ', 'FTX', 'DGQ', 'HJX', 'HRY', 'IOP', 'GJM', 'NQU', 'LTW', 'MOV', 'SUV', 'CLV', 'SUY'],
              ['ADM', 'AIR', 'AQX', 'BEP', 'BJZ', 'BTU', 'CGX', 'CNS', 'FGY', 'DIL', 'DWY', 'EKQ', 'EUV', 'FLM', 'FWY', 'GHN', 'HJR', 'HRZ', 'IOQ', 'JTU', 'KMO', 'CLX', 'KOT', 'NPV', 'PSW', 'SVZ'],
              ['ADN', 'AIZ', 'AQW', 'BEQ', 'BKL', 'BTV', 'CGY', 'CNT', 'FMO', 'DHI', 'DWZ', 'EKR', 'EUW', 'FGL', 'FVZ', 'GNR', 'HJS', 'HTX', 'IOR', 'JMU', 'KPY', 'LPY', 'MOU', 'CJQ', 'PSX', 'SVX'],
              ['ADO', 'AIT', 'ADQ', 'EGR', 'BKM', 'BQW', 'CGZ', 'CNU', 'FNP', 'LOT', 'DXZ', 'EKW', 'EUX', 'FLP', 'FRX', 'GHS', 'HJT', 'HSU', 'BIV', 'IJM', 'CKQ', 'LMZ', 'ORW', 'JNY', 'PVY', 'SVY'],
              ['ADP', 'AIU', 'ADU', 'BES', 'BCK', 'BMX', 'CHI', 'CQY', 'FJR', 'LPX', 'DLQ', 'EKT', 'ERY', 'FOY', 'FXZ', 'GNT', 'HJU', 'GHV', 'IOT', 'JMW', 'KMR', 'LNQ', 'GOW', 'NVZ', 'PSZ', 'SVW'],
              ['AQT', 'AIV', 'AQV', 'BEN', 'BOR', 'BDY', 'CHJ', 'CNW', 'FPR', 'DKL', 'DYZ', 'EKX', 'EHZ', 'FLQ', 'FYZ', 'GIM', 'JOV', 'HSW', 'IOU', 'JMX', 'GKS', 'GLP', 'MPR', 'NTU', 'CTU', 'SWX'],
              ['ARU', 'AIW', 'AQS', 'BEU', 'BKP', 'BTZ', 'JKZ', 'CNX', 'DFQ', 'DLR', 'EFG', 'EKV', 'CUV', 'FLR', 'GHI', 'GNY', 'HPW', 'HSX', 'IOV', 'JMY', 'JTZ', 'LNO', 'MPQ', 'COX', 'DMT', 'SWY'],
              ['AUX', 'AIX', 'ADR', 'BEV', 'BQY', 'BUV', 'CLP', 'CGN', 'FQR', 'DFL', 'DET', 'GIK', 'ERX', 'CFL', 'GHJ', 'OYZ', 'HQW', 'HSY', 'IOW', 'JMZ', 'KMU', 'KNV', 'MPS', 'JNT', 'OPT', 'SWZ'],
              ['ADT', 'AIY', 'AQY', 'BOW', 'BQR', 'BUW', 'CHM', 'CNZ', 'DFS', 'DJL', 'EFI', 'EKU', 'EGV', 'FLT', 'GHK', 'GNP', 'HJY', 'CSZ', 'IOX', 'JNO', 'KMV', 'LUZ', 'MPT', 'RWX', 'PVX', 'QRS'],
              ['ADS', 'AIS', 'AQZ', 'BWX', 'BFK', 'FQX', 'CHN', 'COZ', 'DIV', 'DGO', 'EJK', 'BEY', 'EMT', 'FLU', 'GHL', 'GRV', 'HJW', 'UVX', 'IOY', 'JNP', 'KMW', 'LRT', 'MPU', 'NRT', 'CPY', 'QSZ'],
              ['ADV', 'AJK', 'ARS', 'BRY', 'BCT', 'BUY', 'CHO', 'CFQ', 'DUW', 'DIX', 'EFJ', 'EKZ', 'EWX', 'FLV', 'GHO', 'GJN', 'KLQ', 'HTV', 'IOZ', 'PQW', 'MSX', 'LNU', 'IMP', 'NTZ', 'GPR', 'MSY'],
              ['ADW', 'AJL', 'ART', 'BXZ', 'BKU', 'BCZ', 'CIZ', 'COR', 'DFV', 'DLW', 'EFL', 'EHM', 'EJY', 'FIS', 'GNQ', 'GOP', 'HKX', 'GHT', 'IPQ', 'JQR', 'KMY', 'NOS', 'MPW', 'NVY', 'SUX', 'TUV'],
              ['ADX', 'AJO', 'AQR', 'BFG', 'CKV', 'BVW', 'CHQ', 'COS', 'BTY', 'DXY', 'EFM', 'ENV', 'EWZ', 'FLX', 'GHM', 'GOQ', 'HKN', 'IRT', 'IPR', 'JST', 'KMZ', 'ILN', 'JLP', 'UYZ', 'PUW', 'DSU'],
              ['ASY', 'AFJ', 'AVZ', 'EFU', 'BJK', 'BQV', 'CHR', 'CTZ', 'DIT', 'DLM', 'EFN', 'EQW', 'XYZ', 'DLS', 'GPQ', 'GOR', 'HKO', 'HIM', 'IPS', 'NTW', 'CKO', 'JLX', 'MPY', 'NUX', 'BGR', 'UVW'],
              ['ADJ', 'AJM', 'ARW', 'BFI', 'BKX', 'BVY', 'CQS', 'COU', 'DIQ', 'DGL', 'EFO', 'ELP', 'EXZ', 'FKL', 'HQY', 'GOS', 'HKP', 'HTZ', 'ITV', 'JNX', 'NPR', 'VWY', 'MRZ', 'MNU', 'CGU', 'STW'],
              ['AFV', 'AJP', 'AWX', 'BJL', 'BKY', 'BVZ', 'CHT', 'CEO', 'DFI', 'DMN', 'EPR', 'ELQ', 'OSY', 'DFM', 'HRS', 'GOT', 'HKQ', 'NSW', 'GIU', 'JVX', 'IKX', 'LNZ', 'MQR', 'CUW', 'GPY', 'TUZ'],
              ['AEZ', 'AJX', 'ARY', 'BKS', 'BKZ', 'BIX', 'CHU', 'COT', 'DGH', 'DMO', 'FQV', 'ILY', 'FGT', 'FMX', 'GNS', 'DUY', 'HKR', 'UWZ', 'EIP', 'EJN', 'LNR', 'LOP', 'MQS', 'JVW', 'PQV', 'CTW'],
              ['AEU', 'AJR', 'ARZ', 'BLM', 'BMQ', 'UWY', 'CHV', 'JOX', 'DIS', 'DMP', 'EFR', 'ELS', 'FGI', 'FPY', 'HWZ', 'GOV', 'BGK', 'HUX', 'IPW', 'DJN', 'KNS', 'LOQ', 'NQT', 'CKZ', 'TXY', 'CTV'],
              ['AEI', 'AJS', 'AST', 'BFM', 'KLN', 'BMZ', 'CHW', 'COY', 'DGJ', 'DMQ', 'EFS', 'ELT', 'FGJ', 'BQX', 'GHU', 'OWZ', 'DHK', 'IRX', 'IPX', 'PYZ', 'KNT', 'LOR', 'QUW', 'NUV', 'CPV', 'RVY'],
              ['AEJ', 'AJT', 'ASZ', 'DNR', 'BLO', 'BXY', 'CIX', 'COP', 'DKQ', 'DMR', 'EFT', 'ELU', 'FGQ', 'FMR', 'HSV', 'GMX', 'HKU', 'HSZ', 'IPY', 'IJT', 'KUW', 'GLQ', 'NWY', 'BNV', 'PVZ', 'COW'],
              ['ACE', 'AJU', 'ASV', 'BFO', 'BLS', 'BEZ', 'CHY', 'CPQ', 'DNZ', 'DMS', 'FRU', 'EIV', 'FLN', 'GKQ', 'GHW', 'GMY', 'JKV', 'HWY', 'IRZ', 'JOP', 'KLU', 'DOT', 'IMQ', 'NTX', 'PRX', 'TWX'],
              ['AEL', 'AJV', 'ASU', 'BFP', 'BQZ', 'BOS', 'CHZ', 'CPR', 'DGM', 'DNW', 'EFV', 'ELW', 'KMS', 'FIT', 'GIX', 'GTZ', 'HJK', 'HVX', 'IQR', 'JOQ', 'NRU', 'CLU', 'DMX', 'NOY', 'PWY', 'KTY'],
              ['ABE', 'AJW', 'ASX', 'BFQ', 'BLR', 'CDT', 'CIJ', 'CPS', 'DGN', 'DMU', 'KSV', 'EIL', 'FOR', 'FMU', 'GHY', 'GHP', 'KTZ', 'HVY', 'IQV', 'JOR', 'KNX', 'ELO', 'MQY', 'NWX', 'PUZ', 'TWZ'],
              ['AEN', 'AJQ', 'ABS', 'BJR', 'BGS', 'CDI', 'CIK', 'TVW', 'DOU', 'DMV', 'EFX', 'CEL', 'FGN', 'FMW', 'GHZ', 'PRT', 'HKY', 'HVZ', 'IQU', 'JLO', 'KNY', 'LOW', 'MQZ', 'RUX', 'PSY', 'PTX'],
              ['AEO', 'AJY', 'AKU', 'BRS', 'BLT', 'CDG', 'ILW', 'CPU', 'DGP', 'MVW', 'FNY', 'EHL', 'CFU', 'FMV', 'IJP', 'GSV', 'EHK', 'DWX', 'BIQ', 'JOT', 'KNZ', 'OXY', 'MRS', 'NXZ', 'HQZ', 'QRT'],
              ['AEW', 'AJZ', 'AUV', 'BFT', 'BLU', 'CDH', 'CIR', 'CVX', 'DGX', 'MQX', 'ERZ', 'EMN', 'FGK', 'FMN', 'IKS', 'GPT', 'BHL', 'HVW', 'ISY', 'JOU', 'OPQ', 'LOY', 'DRS', 'NQY', 'PWZ', 'JKT'],
              ['AEQ', 'AKL', 'ATV', 'BFU', 'LUV', 'CDF', 'CIN', 'CPW', 'GJR', 'DJY', 'EGH', 'EMO', 'FGR', 'MXY', 'DKZ', 'BIP', 'HLN', 'HST', 'IQW', 'JNV', 'KOQ', 'SXZ', 'BMU', 'OPY', 'RST', 'WXZ'],
              ['AER', 'AKM', 'ATW', 'BFV', 'BLW', 'CDJ', 'CIO', 'CPX', 'GSY', 'DHZ', 'EIY', 'EPS', 'FSZ', 'FMZ', 'GMN', 'BGV', 'HLO', 'HXY', 'IQX', 'JOW', 'KNR', 'DLP', 'RUV', 'KNU', 'JQT', 'QTU'],
              ['AES', 'AKN', 'ATX', 'BFW', 'BJX', 'CDK', 'CIP', 'CVY', 'DHT', 'DLU', 'EGJ', 'EMQ', 'FTZ', 'FNO', 'BMN', 'GIW', 'HLP', 'HXZ', 'IQY', 'GJV', 'KOS', 'LPR', 'MRW', 'OSZ', 'QRU', 'UVY'],
              ['AGT', 'AKS', 'ATU', 'BFX', 'LMY', 'CDL', 'CIQ', 'CHP', 'ESW', 'DNP', 'BEJ', 'EMR', 'FUV', 'DFN', 'GIO', 'BGX', 'HLQ', 'HYZ', 'IKZ', 'JOY', 'OTW', 'JNS', 'MRX', 'KPW', 'QRV', 'UVZ'],
              ['AEH', 'AKP', 'AHT', 'BFY', 'BLZ', 'CDM', 'CIM', 'CDV', 'GNX', 'DOQ', 'EGL', 'EMS', 'FVW', 'FNQ', 'GPX', 'JYZ', 'HLR', 'IKW', 'IRS', 'JNZ', 'KOU', 'PST', 'RTY', 'BOU', 'QVW', 'JUX'],
              ['AEV', 'AKQ', 'ATY', 'BUZ', 'DUX', 'CDN', 'CIS', 'CHS', 'DJW', 'FRY', 'EGM', 'MTX', 'FGW', 'BFN', 'EIK', 'GPZ', 'HLS', 'IJL', 'HRT', 'JNQ', 'KOV', 'LOU', 'MPZ', 'OPV', 'QRX', 'BWY'],
              ['AEP', 'AWZ', 'AUW', 'BGH', 'BYZ', 'CDO', 'CIT', 'CQT', 'DVX', 'DNS', 'EGN', 'EMU', 'FJX', 'FNS', 'HIV', 'GQR', 'HKL', 'JLM', 'IRU', 'JXY', 'KOW', 'LPV', 'MST', 'KOP', 'QRY', 'BFZ'],
              ['AEX', 'AMZ', 'AKX', 'BRW', 'BMV', 'CDP', 'CIU', 'BCQ', 'DHY', 'DNT', 'EGO', 'EVZ', 'FLY', 'FNT', 'GST', 'GQS', 'HLU', 'IJN', 'IRV', 'JPS', 'KOX', 'LPW', 'HMU', 'FKO', 'QRZ', 'JWY'],
              ['AEY', 'AKR', 'AUY', 'BGJ', 'BFL', 'CDQ', 'CMX', 'CSV', 'DGZ', 'DKN', 'EHP', 'EMW', 'FRZ', 'FNU', 'HIJ', 'GQT', 'HLV', 'BIO', 'IRW', 'JPT', 'KOY', 'LNX', 'MSV', 'OPW', 'QST', 'UXZ'],
              ['AET', 'AKO', 'AUZ', 'GJK', 'BMR', 'CDR', 'CIW', 'CQX', 'DGT', 'DNV', 'EGQ', 'EMX', 'FHI', 'FNV', 'JPU', 'LQS', 'HLW', 'ITY', 'HRX', 'JPV', 'KOZ', 'LUY', 'MSW', 'OPZ', 'BFS', 'BNY'],
              ['AFY', 'AKV', 'AOW', 'BLP', 'GMT', 'CDS', 'CHX', 'CQW', 'DHJ', 'DNU', 'BER', 'EMY', 'FHJ', 'MQU', 'GIV', 'GVZ', 'LOX', 'IJQ', 'IRY', 'NPU', 'BKT', 'LPZ', 'ESX', 'ORT', 'FKS', 'NWZ'],
              ['AFH', 'AYZ', 'AVX', 'BMS', 'BMT', 'CDE', 'CIL', 'CNQ', 'HKT', 'DNX', 'EGU', 'MVZ', 'FKT', 'FNX', 'BGW', 'GUW', 'HJL', 'IJR', 'IUZ', 'JPW', 'KPR', 'LQR', 'EOY', 'OQS', 'OPS', 'DVY'],
              ['AFI', 'AQU', 'AVY', 'BGM', 'MRU', 'CDU', 'BWZ', 'CJX', 'DHP', 'NXY', 'ERT', 'ENO', 'FLZ', 'FNR', 'GHQ', 'DGV', 'HLZ', 'BIJ', 'IST', 'JKP', 'CKP', 'LOS', 'MWY', 'OQT', 'KSX', 'EVW'],
              ['ABF', 'AKW', 'ARV', 'BEW', 'BMP', 'CNV', 'CJK', 'CRS', 'DHM', 'DLZ', 'EGS', 'ENR', 'FHM', 'FNZ', 'GIY', 'GQY', 'HLT', 'IJZ', 'QSU', 'JPX', 'KPT', 'LQT', 'OUW', 'OUX', 'DOY', 'IVX'],
              ['AFK', 'AKT', 'ARX', 'BGP', 'BMW', 'CDW', 'CJL', 'CRT', 'DHN', 'DSY', 'EVY', 'ENQ', 'EFY', 'FJO', 'GIZ', 'GNZ', 'HMO', 'UWX', 'ISV', 'JPZ', 'QUX', 'KLR', 'HMT', 'OSV', 'BIU', 'LPQ'],
              ['AFL', 'ABL', 'AWY', 'BGQ', 'BTX', 'CDX', 'CMZ', 'CRU', 'DHO', 'DNQ', 'ISW', 'ENP', 'FHO', 'FJZ', 'GKU', 'GRS', 'HMP', 'IJV', 'IQS', 'JNR', 'EKP', 'LVY', 'MTW', 'EKO', 'TUX', 'VYZ'],
              ['AFU', 'ALN', 'AKZ', 'PRU', 'BMY', 'CDY', 'BCN', 'CRV', 'DHU', 'BKO', 'DEI', 'EST', 'FHP', 'FGO', 'GJL', 'GRT', 'HMQ', 'IJW', 'ISX', 'JQS', 'PTW', 'KLZ', 'EMV', 'NOX', 'QVZ', 'WXY'],
              ['AFN', 'AIL', 'AXY', 'GIL', 'BPZ', 'DPU', 'CJO', 'CRY', 'BDH', 'STU', 'EKN', 'ETV', 'EFQ', 'FOS', 'JMV', 'GRU', 'HMR', 'IJX', 'DSW', 'QTZ', 'KPX', 'HLM', 'BGN', 'OQY', 'CKW', 'VWZ'],
              ['AFO', 'ALP', 'AXZ', 'ISU', 'BOZ', 'CEF', 'CJP', 'CRX', 'DHR', 'DLO', 'BEG', 'ENU', 'BHR', 'FTV', 'GNW', 'GNV', 'HMS', 'IJY', 'ISZ', 'JQU', 'KMP', 'LQY', 'MTV', 'KQW', 'DTX', 'KWY'],
              ['AFZ', 'ALX', 'AKY', 'BGU', 'BNP', 'CEG', 'CQZ', 'CRW', 'DHS', 'BDX', 'EHI', 'LNV', 'FHS', 'FMP', 'DKO', 'GRW', 'IMV', 'JOZ', 'ITU', 'JQV', 'KNP', 'LQW', 'MTU', 'ORS', 'JTY', 'EXY']
              ]

    print len(groups)
    while len(groups) > 0:
        
        failures = []

        for group in groups:

            random_group = [random_perm(triad) for triad in group]
            first_node = GroupNode(random_group)
#            print first_node.group, first_node.distrib

            fringe = PriorityQueue(min, lambda node: node.score)
            fringe.append(first_node)

            if sum([sum(x) for x in first_node.distrib]) / len(first_node.distrib) == 3:
                goal_score = 0
            else:
                goal_score = len(first_node.distrib)

            visited = []
            while True:

                if len(fringe) == 0:
                    print 'No solutions'
                    break
                node = fringe.pop()
                visited.append(hash(tuple(node.group)))

                if len(visited) >= 10000:
#                    print 'failure!', len(visited)
                    failures.append(node.group)
                    break

                if node.score == goal_score:
#                    print
#                    print
#                    print 'success!', len(visited)
                    print node.group
                    print
                    break

                succs = node.successors()
                new_succs = [x for x in succs if hash(tuple(x.group)) not in visited]

                fringe.extend(new_succs)
                gc.collect()

        groups = failures
        print 'looping', len(failures)

if __name__ == '__main__':
    main()

