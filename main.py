import string
from collections import Counter

# --- Constantes Globales (Se mantienen fuera para que tu lógica original funcione) ---
ALFABETO = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'GN',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
LONGITUD_ALFABETO = 27

FRECUENCIAS_ESPANOLAS = {
    'A': 12.53, 'B': 1.42, 'C': 4.68, 'D': 5.86, 'E': 13.68, 'F': 0.69,
    'G': 1.01, 'H': 0.70, 'I': 6.25, 'J': 0.44, 'K': 0.02, 'L': 4.97,
    'M': 3.15, 'N': 6.71, 
    'GN': 0.31, 
    'O': 8.68, 'P': 2.51, 'Q': 0.88,
    'R': 6.87, 'S': 7.98, 'T': 4.63, 'U': 3.93, 'V': 0.90, 'W': 0.01,
    'X': 0.22, 'Y': 0.90, 'Z': 0.52
}

class CriptoanalisisVigenere:
    def __init__(self):
        self.ALFABETO = ALFABETO
        self.LONGITUD_ALFABETO = len(self.ALFABETO)

        # Frecuencias del inglés (formato decimal)
        self.FRECUENCIAS_INGLES = {
            'A': 0.0817, 'B': 0.0149, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270, 'F': 0.0223,
            'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015, 'K': 0.0077, 'L': 0.0403,
            'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 'P': 0.0193, 'Q': 0.0010, 'R': 0.0599,
            'S': 0.0633, 'T': 0.0906, 'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015,
            'Y': 0.0197, 'Z': 0.0007, 'GN': 0.0001
        }

    # SE AGREGO 'self' A TODOS LOS METODOS
    def formateoDeTexto(self, texto: str) -> list[str]:
        """Limpia el texto de entrada, convirtiéndolo a mayúsculas y filtrando solo caracteres del alfabeto español."""
        texto_formateado = list()
        for char in texto.upper():
            if char == 'Ñ':
                char = 'GN'
            if char in ALFABETO:
                texto_formateado.append(char)
        return texto_formateado 

    def vigenere(self, mensaje: list[str], clave: str, cifrado: bool) -> list[str]:
        """
        Cifra o descifra un mensaje usando el cifrado Vigenère.
        """
        # Se llama a formateoDeTexto usando self
        clave_formateada = self.formateoDeTexto(clave)
        if not clave_formateada:
            return mensaje

        longitudClave = len(clave_formateada)
        resultado = []
        
        for i in range(len(mensaje)):
            letraMensaje = mensaje[i]
            letraClave = clave_formateada[i % longitudClave]   
            
            valorLetraMensaje = ALFABETO.index(letraMensaje)
            valorLetraClave = ALFABETO.index(letraClave)
            
            if cifrado:
                valorCifrado = (valorLetraMensaje + valorLetraClave) % LONGITUD_ALFABETO  
                letraCifrada = ALFABETO[valorCifrado]
                resultado.append(letraCifrada)
            else:
                valorDescifrado = (valorLetraMensaje - valorLetraClave) % LONGITUD_ALFABETO  
                letraDescifrada = ALFABETO[valorDescifrado]  
                resultado.append(letraDescifrada)

        return resultado
    
    def calcularIndiceDeCoincidencias(self, texto):
        counts = Counter(texto)
        tamanioTexto = len(texto) 
        
        if tamanioTexto <= 1: return 0 # Pequeña protección contra división por cero

        numerator = sum(n * (n - 1) for n in counts.values())
        denominator = tamanioTexto * (tamanioTexto - 1)

        return numerator / denominator

    def calcularChiCuadrado(self, text):
        N = len(text)
        if N == 0:
            return 0.0
        
        conteoGeneral = Counter(text)
        valorChiCuadrado = 0.0

        for letra, frecuenciaEsperada in FRECUENCIAS_ESPANOLAS.items():
            conteoParticular = conteoGeneral.get(letra, 0)
            conteoEsperado = N * (frecuenciaEsperada / 100)

            if conteoEsperado == 0:
                continue

            valorChiCuadrado += ((conteoParticular - conteoEsperado) ** 2) / conteoEsperado

        return valorChiCuadrado

    def longitudClave(self, textoCifrado: str, maximaLongitud: int = 20) -> int:
        mejorIC = 0.0
        mejorLongitud = 0
        
        print("Estimando longitud de clave")
        for longitud in range(1, maximaLongitud + 1):
            columnas = [""] * longitud
            for i, caracter in enumerate(textoCifrado):
                columnas[i % longitud] += caracter
            
            # Se llama a calcularIndiceDeCoincidencias usando self
            icPromedio = sum(self.calcularIndiceDeCoincidencias(col) for col in columnas) / longitud
            print(f"Longitud {longitud:2}: IC promedio = {icPromedio:.4f}")
            if icPromedio > mejorIC:
                mejorIC = icPromedio
                mejorLongitud = longitud
                
        print(f"\nLongitud más probable: {mejorLongitud} (IC = {mejorIC:.4f})")
        return mejorLongitud

    def encontrarClave(self, textoCifrado: str, longitudClave: int) -> str:
        columnas = [""] * longitudClave
        for i, caracter in enumerate(textoCifrado):
            columnas[i % longitudClave] += caracter
            
        clave = ""

        print("Estimando Clave")
        for i, col in enumerate(columnas):
            mejorChi = float('inf')
            mejorLetra = ''
            for indice in range(LONGITUD_ALFABETO):
                letraIndice = ALFABETO[indice]
                # Se llama a vigenere usando self
                colDescifrada = self.vigenere(list(col), letraIndice, cifrado = False)
                # Se llama a calcularChiCuadrado usando self
                valorChi = self.calcularChiCuadrado(colDescifrada) 
                
                if valorChi < mejorChi:
                    mejorChi = valorChi
                    mejorLetra = letraIndice
            clave += mejorLetra
            print(f"Columna {i+1:2}/{longitudClave}: Letra de clave encontrada = '{mejorLetra}'")

        print(f"\nClave encontrada: {clave}\n")
        return clave

# --- VARIABLES DE PRUEBA ---
TEXTOAROMPER = """UECWKDVLOTTVACKTPVGEZQMDAMRNPDDUXLBUICAMRHOECBHSPQLVIWO
FFEAILPNTESMLDRUURIFAEQTTPXADWIAWLACCRPBHSRZIVQWOFROGTT
NNXEVIVIBPDTTGAHVIACLAYKGJIEQHGECMESNNOCTHSGGNVWTQHKBPR
HMVUOYWLIAFIRIGDBOEBQLIGWARQHNLOISQKEPEIDVXXNETPAXNZGDX
WWEYQCTIGONNGJVHSQGEATHSYGSDVVOAQCXLHSPQMDMETRTMDUXTEQQ
JMFAEEAAIMEZREGIMUECICBXRVQRSMENNWTXTNSRNBPZHMRVRDYNECG
SPMEAVTENXKEQKCTTHSPCMQQHSQGTXMFPBGLWQZRBOEIZHQHGRTOBSG
TATTZRNFOSMLEDWESIWDRNAPBFOFHEGIXLFVOGUZLNUSRCRAZGZRTTA
YFEHKHMCQNTZLENPUCKBAYCICUBNRPCXIWEYCSIMFPRUTPLXSYCBGCC
UYCQJMWIEKGTUBRHVATTLEKVACBXQHGPDZEANNTJZTDRNSDTFEVPDXK
TMVNAIQMUQNOHKKOAQMTBKOFSUTUXPRTMXBXNPCLRCEAEOIAWGGVVUS
GIOEWLIQFOZKSPVMEBLOHLXDVCYSMGOPJEFCXMRUIGDXNCCRPMLCEWT
PZMOQQSAWLPHPTDAWEYJOGQSOAVERCTNQQEAVTUGKLJAXMRTGTIEAFW
PTZYIPKESMEAFCGJILSBPLDABNFVRJUXNGQSWIUIGWAAMLDRNNPDXGN
PTTGLUHUOBMXSPQNDKBDBTEECLECGRDPTYBVRDATQHKQJMKEFROCLXN
FKNSCWANNAHXTRGKCJTTRRUEMQZEAEIPAWEYPAJBBLHUEHMVUNFRPVM
EDWEKMHRREOGZBDBROGCGANIUYIBNZQVXTGORUUCUTNBOEIZHEFWNBI
GOZGTGWXNRHERBHPHGSIWXNPQMJVBCNEIDVVOAGLPONAPWYPXKEFKOC
MQTRTIDZBNQKCPLTTNOBXMGLNRRDNNNQKDPLTLNSUTAXMNPTXMGEZKA
EIKAGQ"""

TEXTO_EJEMPLO_CLARO = "Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona."

def main():
    # 1. Instanciar la clase
    analizador = CriptoanalisisVigenere()

    # --- Ejemplo de cifrado y descifrado ---
    print("--- EJEMPLO DE CIFRADO/DESCIFRADO ---")
    clave_ejemplo = "SECRETO"
    
    # 2. Llamar a los métodos usando la instancia 'analizador'
    texto_ejemplo_limpio = analizador.formateoDeTexto(TEXTO_EJEMPLO_CLARO)
    
    print(f"Texto original: {''.join(texto_ejemplo_limpio)}")
    print(f"Clave: {clave_ejemplo}")

    texto_cifrado_ejemplo = analizador.vigenere(texto_ejemplo_limpio, clave_ejemplo, True)
    print(f"Texto cifrado: {''.join(texto_cifrado_ejemplo)}")

    texto_descifrado_ejemplo = analizador.vigenere(texto_cifrado_ejemplo, clave_ejemplo, False)
    print(f"Texto descifrado: {''.join(texto_descifrado_ejemplo)}\n")

    # --- Análisis para romper el cifrado de TEXTOAROMPER ---
    print("--- ANÁLISIS DE TEXTOAROMPER ---")
    
    textoLimpioARomper = analizador.formateoDeTexto(TEXTOAROMPER)
    
    # Llamamos a longitudClave a través de la instancia
    longitud = analizador.longitudClave(textoLimpioARomper)
    
    # Llamamos a encontrarClave a través de la instancia
    clave = analizador.encontrarClave(textoLimpioARomper, longitud)
    
    # Desciframos usando la instancia
    texto = analizador.vigenere(textoLimpioARomper, clave, False)
    
    print("Texto final descifrado de TEXTOAROMPER:")
    for letra in texto:
        print(letra, end="")
    print("\n")

if __name__ == "__main__":
    main()