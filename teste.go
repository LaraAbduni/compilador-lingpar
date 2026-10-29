var b int = 5 // Variável Global

func soma(x int, y int) int {
  var a int // Variável Local
  a = x + y
  Println(a) // Imprime 7
  return a
}

func main() {
  var a int
  {
    var b int
    a = 3
    b = soma(a, 4)
    Println(b) // Imprime 7
  }
  Println(a) // Imprime 3
  Println(b) // Imprime 5
}
