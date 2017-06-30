
import org.apache.spark.sql._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.types._
import org.apache.spark.sql.catalyst.encoders.ExpressionEncoder
import org.apache.spark.sql.Encoder
import org.apache.spark.sql.streaming.OutputMode._
import org.apache.spark.sql.streaming.ProcessingTime
import scala.concurrent.duration._

object Ex03_DiretorioLocalStream {

  def main(){
/*
    if (args.length < 1) {
      System.err.println("Usage: Ex03_DiretorioLocalStream diretorio")
      System.exit(1)
    }
*/
  //  val diretorio : String = args(0)
    val diretorio : String = "canal"

    Logger.getLogger("org").setLevel(Level.ERROR)

    val spark = SparkSession
      .builder
      .master("local[*]")
      .appName("transmissao")
      .getOrCreate()

    import spark.implicits._


    val esquema = new StructType()
      .add("categoria","string")
    	.add("timestamp","string")
    	.add("validade","string")
      .add("preco","string")
      .add("mercado","string")
      .add("titulo","string")


    val leituras = spark.readStream
		.schema(esquema)
    	.json(diretorio)

    val atividades = leituras.select($"titulo",$"preco").as[Leitura]

    val contagens = atividades.groupBy("titulo","preco")
    	.count
    	.withColumnRenamed("count","leituras")
    	.orderBy($"titulo",$"preco".desc)

    val query = contagens.writeStream
      .outputMode(Complete)
      .trigger(ProcessingTime(5.seconds))
      .format("console")
      .start

	query.awaitTermination()
  }
}
