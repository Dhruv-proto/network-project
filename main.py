import dpkt
import socket
import pygeoip
gi=pygeoip.GeoIP('GeoLiteCity.dat')
def retkml(dstip,srcip):
    dst=gi.record_by_name(dstip)
    src=gi.record_by_name('103.212.208.188')
    try:
        dstlatitude=dst['latitude']
        dstlongitude=dst['longitude']
        srclatitude=src['latitude']
        srclongitude=src['longitude']
        kml=(
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''
def plotIPs(pcap):
    kmlpts=''
    for (ts,buf) in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(buf)
            ip=eth.data
            src=socket.inet_ntoa(ip.src)
            dst=socket.inet_ntoa(ip.dst)
            KML=retkml(dst,src)
            kmlpts=kmlpts+KML
        except:
            pass
    return kmlpts
def main():
    f= open('data.pcap','rb')
    pcap=dpkt.pcap.Reader(f)
    kmlheader='<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter= '</Document>\n</kml>\n'
    kmldoc= kmlheader+plotIPs(pcap)+kmlfooter
    print(kmldoc)
if __name__ == '__main__':
    main()