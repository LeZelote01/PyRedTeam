import unittest
from unittest.mock import patch, MagicMock
from modules.network.port_scan import Attack

class TestPortScan(unittest.TestCase):
    # Test quand un port est ouvert
    @patch('socket.socket')  # Mock du socket
    def test_port_scan_open(self, mock_socket):
        mock_sock = MagicMock()  # Création du mock
        mock_socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0  # Simule un port ouvert
        
        attack = Attack()
        attack.setup(target_ip="127.0.0.1", ports="80")
        result = attack.execute()
        
        self.assertEqual(result, {"open_ports": [80]})
        attack.cleanup()

    # Test quand un port est fermé
    @patch('socket.socket')
    def test_port_scan_closed(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 1  # Simule un port fermé
        
        attack = Attack()
        attack.setup(target_ip="127.0.0.1", ports="80")
        result = attack.execute()
        
        self.assertEqual(result, {"open_ports": []})
        attack.cleanup()

    # Test du parseur de ports
    def test_port_parser(self):
        attack = Attack()
        
        # Test plage de ports
        ports = attack._parse_ports("1-3")
        self.assertEqual(ports, [1,2,3])
        
        # Test ports individuels
        ports = attack._parse_ports("80,443")
        self.assertEqual(ports, [80, 443])
        
        # Test mixte
        ports = attack._parse_ports("80,443,8080-8082")
        self.assertEqual(ports, [80, 443, 8080, 8081, 8082])

if __name__ == '__main__':
    unittest.main()  # Lance les tests