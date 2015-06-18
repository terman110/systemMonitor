import wmi
import psutil
import time
import math
import socket

def hostName():
  return socket.gethostname()

# https://msdn.microsoft.com/en-us/library/aa394173(v=vs.85).aspx
# [Provider("CIMWin32")]class Win32_LogicalDisk : CIM_LogicalDisk
# {
#   uint16   Access;
#   uint16   Availability;
#   uint64   BlockSize;
#   string   Caption;
#   boolean  Compressed;
#   uint32   ConfigManagerErrorCode;
#   boolean  ConfigManagerUserConfig;
#   string   CreationClassName;
#   string   Description;
#   string   DeviceID;
#   uint32   DriveType;
#   boolean  ErrorCleared;
#   string   ErrorDescription;
#   string   ErrorMethodology;
#   string   FileSystem;
#   uint64   FreeSpace;
#   datetime InstallDate;
#   uint32   LastErrorCode;
#   uint32   MaximumComponentLength;
#   uint32   MediaType;
#   string   Name;
#   uint64   NumberOfBlocks;
#   string   PNPDeviceID;
#   uint16   PowerManagementCapabilities[];
#   boolean  PowerManagementSupported;
#   string   ProviderName;
#   string   Purpose;
#   boolean  QuotasDisabled;
#   boolean  QuotasIncomplete;
#   boolean  QuotasRebuilding;
#   uint64   Size;
#   string   Status;
#   uint16   StatusInfo;
#   boolean  SupportsDiskQuotas;
#   boolean  SupportsFileBasedCompression;
#   string   SystemCreationClassName;
#   string   SystemName;
#   boolean  VolumeDirty;
#   string   VolumeName;
#   string   VolumeSerialNumber;
# };
class memSize:
  __size = 0
  __unit = 'Bytes'
  __bytes = 0
  __base = 1024
  
  def __init__(self, s_bytes, base = 1024):
    self.__base = base
    self.__parse(s_bytes, base)
    
  def __parse(self, s_bytes, base = 1024):
    s_bytes = float(s_bytes)
    self.__bytes = s_bytes
    if s_bytes < base:
      self.__size = s_bytes
      self.__unit = 'Bytes'
      return
    s_bytes /= base
    if s_bytes < base:
      self.__size = s_bytes
      self.__unit = 'KB'
      return
    s_bytes /= base
    if s_bytes < base:
      self.__unit = 'MB'
      self.__size = s_bytes
      return
    s_bytes /= base
    if s_bytes < base:
      self.__unit = 'GB'
      self.__size = s_bytes
      return
    s_bytes /= base
    if s_bytes < base:
      self.__unit = 'TB'
      self.__size = s_bytes
      return
    s_bytes /= base
    self.__size = s_bytes
    self.__unit = 'PB'
    
  def bytes(self):
    return self.__bytes
    
  def size(self,precision = 2):
    return str('{:.'+str(int(precision))+'f}').format(self.__size)
  
  def unit(self):
    return self.__unit
  
  def string(self,precision = 2):
    return self.size(precision) + self.unit()
  
def parseDrives(onlyLocal=True):
    
  types = {
  0: "Unknown",
  1: "No Root Directory",
  2: "Removable Disk",
  3: "Local Disk",
  4: "Network Drive",
  5: "Compact Disc",
  6: "RAM Disc"
  } 
    
  rlist = []
  if onlyLocal:
    disks = wmi.WMI().Win32_LogicalDisk(DriveType=3)
  else:
    disks = wmi.WMI().Win32_LogicalDisk()
  for disk in disks:
    space = 100. * float(disk.FreeSpace) / float(disk.Size)
    rlist.append( {
	"Name": disk.VolumeName, 
	"Letter": disk.Caption, 
	"FreeInt": int(disk.FreeSpace), 
	"SizeInt": int(disk.Size),
	"UsedInt": int(disk.Size) - int(disk.FreeSpace), 
	"Free": memSize(disk.FreeSpace),
	"Size": memSize(disk.Size),
	"Used": memSize(int(disk.Size)-int(disk.FreeSpace)),
	"FreePrcnt": 100. * float(disk.FreeSpace) / float(disk.Size),
	"UsedPrcnt": 100. * float(int(disk.Size)-int(disk.FreeSpace)) / float(disk.Size),
	"Type": types[disk.DriveType]
	} )
  return rlist

# https://msdn.microsoft.com/en-us/library/aa394493(v=vs.85).aspx
# [Provider("CIMWin32")]class Win32_TemperatureProbe : CIM_TemperatureSensor
# {
#   sint32   Accuracy;
#   uint16   Availability;
#   string   Caption;
#   uint32   ConfigManagerErrorCode;
#   boolean  ConfigManagerUserConfig;
#   string   CreationClassName;
#   sint32   CurrentReading;
#   string   Description;
#   string   DeviceID;
#   boolean  ErrorCleared;
#   string   ErrorDescription;
#   datetime InstallDate;
#   boolean  IsLinear;
#   uint32   LastErrorCode;
#   sint32   LowerThresholdCritical;
#   sint32   LowerThresholdFatal;
#   sint32   LowerThresholdNonCritical;
#   sint32   MaxReadable;
#   sint32   MinReadable;
#   string   Name;
#   sint32   NominalReading;
#   sint32   NormalMax;
#   sint32   NormalMin;
#   string   PNPDeviceID;
#   uint16   PowerManagementCapabilities[];
#   boolean  PowerManagementSupported;
#   uint32   Resolution;
#   string   Status;
#   uint16   StatusInfo;
#   string   SystemCreationClassName;
#   string   SystemName;
#   sint32   Tolerance;
#   sint32   UpperThresholdCritical;
#   sint32   UpperThresholdFatal;
#   sint32   UpperThresholdNonCritical;
# };
# print (w[0].CurrentTemperature/10.0)
# probes = wmi.WMI().Win32_TemperatureProbe()
# for probe in probes:
  # print(probe)
# values = wmi.WMI(namespace="root\\wmi").MSAcpi_ThermalZoneTemperature()
# for value in values:
  # print(value)
# print('-----------------------------------------------------------------------')

# https://msdn.microsoft.com/en-us/library/aa394217(v=vs.85).aspx
# [Provider("CIMWin32")]class Win32_NetworkAdapterConfiguration : CIM_Setting
# {
#   boolean  ArpAlwaysSourceRoute;
#   boolean  ArpUseEtherSNAP;
#   string   Caption;
#   string   DatabasePath;
#   boolean  DeadGWDetectEnabled;
#   string   DefaultIPGateway[];
#   uint8    DefaultTOS;
#   uint8    DefaultTTL;
#   string   Description;
#   boolean  DHCPEnabled;
#   datetime DHCPLeaseExpires;
#   datetime DHCPLeaseObtained;
#   string   DHCPServer;
#   string   DNSDomain;
#   string   DNSDomainSuffixSearchOrder[];
#   boolean  DNSEnabledForWINSResolution;
#   string   DNSHostName;
#   string   DNSServerSearchOrder[];
#   boolean  DomainDNSRegistrationEnabled;
#   uint32   ForwardBufferMemory;
#   boolean  FullDNSRegistrationEnabled;
#   uint16   GatewayCostMetric[];
#   uint8    IGMPLevel;
#   uint32   Index;
#   uint32   InterfaceIndex;
#   string   IPAddress[];
#   uint32   IPConnectionMetric;
#   boolean  IPEnabled;
#   boolean  IPFilterSecurityEnabled;
#   boolean  IPPortSecurityEnabled;
#   string   IPSecPermitIPProtocols[];
#   string   IPSecPermitTCPPorts[];
#   string   IPSecPermitUDPPorts[];
#   string   IPSubnet[];
#   boolean  IPUseZeroBroadcast;
#   string   IPXAddress;
#   boolean  IPXEnabled;
#   uint32   IPXFrameType[];
#   uint32   IPXMediaType;
#   string   IPXNetworkNumber[];
#   string   IPXVirtualNetNumber;
#   uint32   KeepAliveInterval;
#   uint32   KeepAliveTime;
#   string   MACAddress;
#   uint32   MTU;
#   uint32   NumForwardPackets;
#   boolean  PMTUBHDetectEnabled;
#   boolean  PMTUDiscoveryEnabled;
#   string   ServiceName;
#   string   SettingID;
#   uint32   TcpipNetbiosOptions;
#   uint32   TcpMaxConnectRetransmissions;
#   uint32   TcpMaxDataRetransmissions;
#   uint32   TcpNumConnections;
#   boolean  TcpUseRFC1122UrgentPointer;
#   uint16   TcpWindowSize;
#   boolean  WINSEnableLMHostsLookup;
#   string   WINSHostLookupFile;
#   string   WINSPrimaryServer;
#   string   WINSScopeID;
#   string   WINSSecondaryServer;
# };
def ip():
  rlist = []
  for interface in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1):
    #print(interface.Description+" ("+interface.MACAddress+")")
    for ip_address in interface.IPAddress:
      rlist.append( ip_address)
  return rlist

# https://msdn.microsoft.com/en-us/library/aa394373(v=vs.85).aspx
# [Provider("CIMWin32")]class Win32_Processor : CIM_Processor
# {
#   uint16   AddressWidth;
#   uint16   Architecture;
#   string   AssetTag;
#   uint16   Availability;
#   string   Caption;
#   uint32   Characteristics;
#   uint32   ConfigManagerErrorCode;
#   boolean  ConfigManagerUserConfig;
#   uint16   CpuStatus;
#   string   CreationClassName;
#   uint32   CurrentClockSpeed;
#   uint16   CurrentVoltage;
#   uint16   DataWidth;
#   string   Description;
#   string   DeviceID;
#   boolean  ErrorCleared;
#   string   ErrorDescription;
#   uint32   ExtClock;
#   uint16   Family;
#   datetime InstallDate;
#   uint32   L2CacheSize;
#   uint32   L2CacheSpeed;
#   uint32   L3CacheSize;
#   uint32   L3CacheSpeed;
#   uint32   LastErrorCode;
#   uint16   Level;
#   uint16   LoadPercentage;
#   string   Manufacturer;
#   uint32   MaxClockSpeed;
#   string   Name;
#   uint32   NumberOfCores;
#   uint32   NumberOfEnabledCore;
#   uint32   NumberOfLogicalProcessors;
#   string   OtherFamilyDescription;
#   string   PartNumber;
#   string   PNPDeviceID;
#   uint16   PowerManagementCapabilities[];
#   boolean  PowerManagementSupported;
#   string   ProcessorId;
#   uint16   ProcessorType;
#   uint16   Revision;
#   string   Role;
#   boolean  SecondLevelAddressTranslationExtensions;
#   string   SerialNumber;
#   string   SocketDesignation;
#   string   Status;
#   uint16   StatusInfo;
#   string   Stepping;
#   string   SystemCreationClassName;
#   string   SystemName;
#   uint32   ThreadCount;
#   string   UniqueId;
#   uint16   UpgradeMethod;
#   boolean  VirtualizationFirmwareEnabled;
#   string   Version;
#   boolean  VMMonitorModeExtensions;
#   uint32   VoltageCaps;
# };
def cpuLoad(interv):
  return psutil.cpu_percent(interval=int(interv), percpu=True)

def uptime():
  def elapsedString(sec):
    sec = math.floor( float( sec))
    s = sec%60
    m = math.floor(sec/60)
    h = math.floor(m/60)
    m = m%60
    return '{}:{}:{}'.format(h,m,s)
  elapsed = time.time() - psutil.boot_time()
  return elapsedString(elapsed)

def now():
  return time.strftime("%d.%m.%Y %H:%M", time.localtime())