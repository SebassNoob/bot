import java.sql.*;
import java.util.*;

public class SetupDb{
  private static HashMap<String, String> databases(){
    HashMap<String, String> temp = new HashMap<>();
    temp.put("./other/snipe2.db", "./other/snipe2.sql");
    temp.put("./other/serverSettings.db", "./other/serverSettings.sql");
    temp.put("./other/userSettings.db", "./other/userSettings.sql");
    return temp;
  }
  public static void main(String[] args){
    System.out.println(SetupDb.databases());
  }
}