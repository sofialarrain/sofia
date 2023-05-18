import unittest
from desencriptar import deserializar_diccionario, decodificar_largo, \
    separar_msg_encriptado, decodificar_secuencia, desencriptar
from encriptar import serializar_diccionario, encriptar
from errors import JsonError


class TestDesencriptar(unittest.TestCase):
    def test_deserializar_diccionario(self):
        test_1 = deserializar_diccionario(bytearray(b'{"user": "name"}'))
        test_2 = deserializar_diccionario(
            bytearray(b'{"1": [1, 2], "2": "\\u00e1\\u00e9\\u00ed"}'))
        res_1 = {"user": "name"}
        res_2 = {"1": [1, 2], "2": "áéí"}

        # Verificar tipo de dato pedido
        self.assertIsInstance(test_1, dict)
        # Verificar excepciones
        self.assertRaises(JsonError, deserializar_diccionario, b'{123:}')
        # Verificar resultados
        self.assertDictEqual(test_1, res_1)
        self.assertDictEqual(test_2, res_2)

    def test_decodificar_largo(self):
        test_1 = decodificar_largo(bytearray(b'\x00\x10\x00\t'))
        test_2 = decodificar_largo(bytearray(b'\xA0\xA0\x11\\'))

        res_1 = 1048585
        res_2 = 2694844764
        # Verificar tipo de dato pedido
        self.assertIsInstance(test_1, int)
        # Verificar resultados
        self.assertEqual(test_1, res_1)
        self.assertEqual(test_2, res_2)

    def test_separar_msg_encriptado(self):
        test_1 = separar_msg_encriptado(
            bytearray(b'\x00\x00\x00\x02\x01\x03\x00\x02\x05\x00\x01\x00\x03'))
        test_2 = separar_msg_encriptado(
            bytearray(b'\x00\x00\x00\x01\x03\x00\x01\x02\xaa\x00\x03'))

        res_1 = [bytearray(b'\x01\x03'), bytearray(
            b'\x00\x02\x05'), bytearray(b'\x00\x01\x00\x03')]
        res_2 = [bytearray(b'\x03'), bytearray(
            b'\x00\x01\x02\xaa'), bytearray(b'\x00\x03')]
        # Verificar tipo de dato pedido
        self.assertIsInstance(res_1, list)
        # Verificar resultados
        self.assertListEqual(test_1, res_1)
        self.assertListEqual(test_2, res_2)

    def test_decodificar_secuencia(self):
        test_1 = decodificar_secuencia(bytearray(b'\x00\x01\x00\x02\x00\x03'))
        test_2 = decodificar_secuencia(bytearray(b'\x00\x0b\x11\\\x00c'))

        res_1 = [1, 2, 3]
        res_2 = [11, 4444, 99]
        # Verificar tipo de dato pedido
        self.assertIsInstance(res_1, list)
        # Verificar resultados
        self.assertListEqual(test_1, res_1)
        self.assertListEqual(test_2, res_2)

    def test_desencriptar(self):
        test_1 = desencriptar(
            bytearray(b'\x00\x00\x00\x02\x01\x03\x00\x02\x05\x00\x01\x00\x03'))
        test_2 = desencriptar(
            bytearray(b'\x00\x00\x00\x01\x03\x00\x01\x02\xaa\x00\x03'))
        res_1 = bytearray(b'\x00\x01\x02\x03\x05')
        res_2 = bytearray(b'\x00\x01\x02\x03\xAA')

        # Verificar tipo de dato pedido
        self.assertIsInstance(res_1, bytearray)
        # Verificar resultados
        self.assertEqual(test_1, res_1)
        self.assertEqual(test_2, res_2)

    def test_desencriptar_2(self):
        test_1 = desencriptar(
            bytearray(b'\x00\x00\x00\x02\x02\x03\x02\x01\x05\x00\x02\x00\x03'))
        test_2 = desencriptar(
            bytearray(b'\x00\x00\x00\x03\x02\x01\x10\x03\xaa\x00\x02\x00\x01\x00\x00'))
        res_1 = bytearray(b'\x02\x01\x02\x03\x05')
        res_2 = bytearray(b'\x10\x01\x02\x03\xAA')

        # Verificar tipo de dato pedido
        self.assertIsInstance(res_1, bytearray)
        # Verificar resultados
        self.assertEqual(test_1, res_1)
        self.assertEqual(test_2, res_2)

    def test_desencriptar_3(self):
        test_1 = desencriptar(
            bytearray(b'\x00\x00\x00\x04dc3sasdeng12a21\x00\x02\x00\
\x03\x00\n\x00\x0c'))
        test_2 = desencriptar(
            bytearray(b'\x00\x00\x00\x05yna94aforger1234spy9x99family\
\x00\x02\x00\x01\x00\x00\x00\x13\x00\x04'))
        res_1 = bytearray(b'asdcdeng123as21')
        res_2 = bytearray(b'anya4forger1234spy99x99family')

        # Verificar tipo de dato pedido
        self.assertIsInstance(res_1, bytearray)
        # Verificar resultados
        self.assertEqual(test_1, res_1)
        self.assertEqual(test_2, res_2)

    def test_secuencia_completa(self):
        test = {"anime": "chainsawman", "year": 2022}
        encriptado = encriptar(serializar_diccionario(test), [0, 6, 1, 4, 7])
        desencriptado = desencriptar(encriptado)
        resultado_final = deserializar_diccionario(desencriptado)
        self.assertEqual(test, resultado_final)

    def test_secuencia_completa_2(self):
        test = {"1": [1, 2], "2": "áéí"}
        encriptado = encriptar(serializar_diccionario(test), [1, 3, 9, 12])
        desencriptado = desencriptar(encriptado)
        resultado_final = deserializar_diccionario(desencriptado)
        self.assertEqual(test, resultado_final)

    def test_secuencia_completa_3(self):
        test = {"anime": "gintama", "anime2": "code geass"}
        encriptado = encriptar(serializar_diccionario(test), [
                               12, 1, 5, 8, 2, 7, 4])
        desencriptado = desencriptar(encriptado)
        resultado_final = deserializar_diccionario(desencriptado)
        self.assertEqual(test, resultado_final)


if __name__ == '__main__':
    unittest.main(verbosity=2)
