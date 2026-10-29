var global int = 10

func subtrai(a int, b int) int {
  return a - b
}

func fibonacci(n int) int {
  if n < 2 {
    return n
  }
  return fibonacci(n - 1) + fibonacci(n - 2)
}

func soma_global(x int) int {
  return global + x
}

func main() {
  Println(subtrai(10, 3))
  Println(fibonacci(6))
  Println(soma_global(5))
}
