func fatorial(n int) int {
  if n < 2 {
    return 1
  }
  return n * fatorial(n - 1)
}

func main() {
  Println(fatorial(5))
}
