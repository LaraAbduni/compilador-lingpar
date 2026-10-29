type A struct {
  var b int
}

type Interna struct {
  var valor int
}

type Externa struct {
  var interna Interna
  var ativo bool
}

func main() {
  var x A
  x.b = 1
  Println(x.b)

  var primeira Externa
  var segunda Externa
  primeira.interna.valor = 7
  primeira.ativo = true

  Println(primeira.interna.valor)
  Println(primeira.ativo)
  Println(segunda.interna.valor)
  Println(segunda.ativo)
}
