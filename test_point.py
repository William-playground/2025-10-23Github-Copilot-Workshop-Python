import unittest
from point import Point2D


class TestPoint2D(unittest.TestCase):
    """point.pyモジュールのテストクラス"""
    
    def test_distance_to_basic(self):
        """基本的な距離計算のテスト"""
        p1 = Point2D(0, 0)
        p2 = Point2D(3, 4)
        self.assertEqual(p1.distance_to(p2), 5.0)
    
    def test_distance_to_same_point(self):
        """同じ点の距離はゼロであることをテスト"""
        p1 = Point2D(5, 5)
        p2 = Point2D(5, 5)
        self.assertEqual(p1.distance_to(p2), 0.0)
    
    def test_distance_to_negative_coordinates(self):
        """負の座標での距離計算のテスト"""
        p1 = Point2D(-1, -1)
        p2 = Point2D(2, 3)
        expected = ((2 - (-1))**2 + (3 - (-1))**2)**0.5
        self.assertAlmostEqual(p1.distance_to(p2), expected)
    
    def test_str_representation(self):
        """文字列表現のテスト"""
        p = Point2D(10, 20)
        self.assertEqual(str(p), "Point2D(10, 20)")


if __name__ == '__main__':
    unittest.main()
