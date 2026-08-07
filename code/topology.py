
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
class LFATopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
def run():
    setLogLevel('info')
    topo = LFATopo()
    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        waitConnected=False
    )
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )
    net.start()
    print("\n=== Network Started ===")
    print("Hosts:")
    print("  h1 = 10.0.0.1 (Attacker 1)")
    print("  h2 = 10.0.0.2 (Attacker 2)")
    print("  h3 = 10.0.0.3 (Victim 1)")
    print("  h4 = 10.0.0.4 (Victim 2)")
    print("\nSwitches: s1─s2─s3─s4 (Linear)")
    print("Bottleneck: s2─s3 link")
    print("\nRun these commands:")
    print("  pingall")
    print("  h3 iperf -s -p 5001 &")
    print("  h4 iperf -s -p 5001 &")
    print("  h1 iperf -c 10.0.0.3 -p 5001 -t 30 -b 2M &")
    print("  h2 iperf -c 10.0.0.4 -p 5001 -t 30 -b 2M &")
    print("  h1 hping3 -S --flood -p 80 10.0.0.3 &")
    print("  h2 hping3 -S --flood -p 80 10.0.0.4 &")
    print("=======================\n")
    CLI(net)
    net.stop()
if __name__ == '__main__':
    run()

