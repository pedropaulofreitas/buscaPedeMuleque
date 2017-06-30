/* main.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf


// passar keyword e calcular as paradas basedo nela

object SimpleApp {
  def main(args: Array[String]) {
    val logFile = "file.json" // arquivo json de onde extrairemos as estatisticas
    val conf = new SparkConf().setAppName("Simple Application")
    val sc = new SparkContext(conf)
    val logData = sc.textFile(logFile, 2).cache()

    val numAs = logData.filter(line => line.contains("Feijao")).count()
    val numBs = logData.filter(line => line.contains("Arroz")).count()

    /*selecionando todas as linhas que contem arroz e calculando metricas*/
    val arrozs = logData.filter(line => line.contains("Arroz"))

  //  val expressao = """([\n\r].*"preco"\s*([^\n]*))\w+/g""".r
  //  val expressao = preco

    // arrozs foreach { line =>
    //    expressao findFirstIn line foreach { preco => println(preco) }
    //  }
    //    precos.take(5).foreach(println)

    //val precos = arrozs.map(line => line)
    //val linha = arrozs.take(1)
    val precos = arrozs.map(L => (L.split("\"")(15)))
    //precos foreach(println)

    precos.foreach(println)
    precos.saveAsTextFile("precos/precos.txt")
    //println(precos)
    println(s"Lines with Feijao: $numAs, Lines with Arroz: $numBs")
    sc.stop()
  }
}
