# RubicsCubeRL - A research journey into games and RL in general

 fun fact => rubic's cube has 4.3e19 possible states but it takes at max 26 operations to solve it !!!

 Let's teach my machine how to solve rubics cube with similar order moves !

 operation set = {'F','U','R','D','L','B','~F','~U','~R','~D','~L','~B'}

    cube = {
      0: array([[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]),
      1: array([[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]]),
      2: array([[2, 2, 2],
                [2, 2, 2],
                [2, 2, 2]]),
      3: array([[3, 3, 3],
                [3, 3, 3],
                [3, 3, 3]]),
      4: array([[4, 4, 4],
                [4, 4, 4],
                [4, 4, 4]]),
      5: array([[5, 5, 5],
                [5, 5, 5],
                [5, 5, 5]])
    }
