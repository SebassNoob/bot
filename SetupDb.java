
import java.sql.*;
import java.util.*;
import java.io.*;

public class SetupDb{

  public static HashMap<String,String> getFilePaths(){
    HashMap<String, String> filepaths = new HashMap<>();
    filepaths.put("./other/snipe2.db", "./other/snipe2.sql");
    filepaths.put("./other/serverSettings.db", "./other/serverSettings.sql");
    filepaths.put("./other/userSettings.db", "./other/userSettings.sql");
    return filepaths;
  }
  
  
  
  
  private static Connection connect(String filename) throws SQLException{
    String url = "jdbc:sqlite:"+filename;
    Connection conn = DriverManager.getConnection(url);
    
    if (conn != null) {
      System.out.println("Created file at " + filename);
    }
    
      
    
    return conn;
  }
  
  private static void createTable(Connection conn, String readFrom) throws FileNotFoundException, IOException{
    
    FileReader fr = new FileReader(readFrom);
    StringBuilder s = new StringBuilder();
    int c; // decl var for indiv char in stream
    while ((c = fr.read())!= -1){
      
      s.append((char) c);
    }
    fr.close();
    String sql = s.toString();
    
    
    try (Statement stmt = conn.createStatement()){
      stmt.executeUpdate(sql);
      System.out.println("Executed in "+ conn.getMetaData().getURL() + ":");
      System.out.println(sql);
    } catch (SQLException e) {
      throw new RuntimeException("Error executing sql:\n" + sql, e);
    }
    
  }
  
  public static void main(String[] args) throws Exception{
    Class.forName("org.sqlite.JDBC"); //make sure its there
    
    for (Map.Entry<String,String> entry: getFilePaths().entrySet()){
      Connection conn = connect(entry.getKey());
      createTable(conn, entry.getValue());
    }
    
  }
}