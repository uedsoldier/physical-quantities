import unittest
from fractions import Fraction
# Asegúrate de importar tu clase Dimension
from core.unit import Dimensions 

class TestFractionalDimensions(unittest.TestCase):

    def test_initialization_with_floats_converts_to_fraction(self):
        """Prueba que inicializar con 0.5 se convierte internamente a 1/2."""
        d = Dimensions({'L': 0.5})
        
        # Verificamos que internamente sea una Fracción, no un float
        self.assertIsInstance(d._dimensions_dict['L'], Fraction)
        self.assertEqual(d._dimensions_dict['L'], Fraction(1, 2))
        
        # Verificamos la representación en string
        self.assertEqual(str(d), 'L^1/2')

    def test_square_root_operation(self):
        """Prueba que elevar a la 0.5 genere fracciones exactas."""
        L = Dimensions({'L': 1})
        
        # Operación: L^1 ** 0.5
        sqrt_L = L ** 0.5
        
        self.assertEqual(sqrt_L, Dimensions({'L': Fraction(1, 2)}))
        self.assertEqual(str(sqrt_L), 'L^1/2')

    def test_reversibility_of_roots(self):
        """Prueba que (L^0.5 * L^0.5) restaure L^1 exacto."""
        half_L = Dimensions({'L': 0.5})
        
        # Multiplicamos: L^0.5 * L^0.5 = L^1.0
        full_L = half_L * half_L
        
        # Debe ser exactamente igual a una dimensión entera
        self.assertEqual(full_L, Dimensions({'L': 1}))
        # El string no debe mostrar 'L^1.0' ni 'L^1', solo 'L'
        self.assertEqual(str(full_L), 'L')

    def test_precision_thirds(self):
        """
        Prueba CRÍTICA: Verifica que usar Fractions evita errores de punto flotante.
        1/3 + 1/3 + 1/3 debe ser exactamente 1, no 0.999999...
        """
        # T^(1/3)
        d_third = Dimensions({'T': Fraction(1, 3)})
        
        # T^(1/3) * T^(1/3) * T^(1/3)
        d_result = d_third * d_third * d_third
        
        self.assertEqual(d_result, Dimensions({'T': 1}))
        self.assertTrue(d_result._dimensions_dict['T'].denominator == 1)

    def test_fracture_mechanics_scenario(self):
        """
        Caso real de ingeniería: Tenacidad de Fractura (K).
        Fórmula: K = Stress * sqrt(Length)
        Unidades: (M * L^-1 * T^-2) * (L^0.5) = M * L^-0.5 * T^-2
        """
        stress = Dimensions({'M': 1, 'L': -1, 'T': -2})
        sqrt_length = Dimensions({'L': 0.5})
        
        k_factor = stress * sqrt_length
        
        # Verificamos el resultado matemático
        expected = Dimensions({'M': 1, 'L': -0.5, 'T': -2})
        self.assertEqual(k_factor, expected)
        
        # Verificamos que el string se vea "científico"
        # Orden esperado (alfabético o tu custom MLT): L, M, T
        # L^-1/2 * M * T^-2
        self.assertIn('L^-1/2', str(k_factor))
        self.assertIn('M', str(k_factor))
        self.assertIn('T^-2', str(k_factor))

    def test_mixed_arithmetic(self):
        """Prueba mezclar enteros, floats y fractions en una sola operación."""
        d1 = Dimensions({'A': 1})            # Entero
        d2 = Dimensions({'A': 0.5})          # Float
        d3 = Dimensions({'A': Fraction(3, 2)}) # Fracción (1.5)
        
        # 1 + 0.5 - 1.5 = 0
        result = (d1 * d2) / d3
        
        self.assertTrue(result.is_dimensionless)
        self.assertEqual(str(result), "dimensionless")

if __name__ == '__main__':
    unittest.main()