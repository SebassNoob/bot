package other;


import javax.net.ssl.*;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.Executors;
// javac other/Backups.java
// java other.Backups

public class Backups{

  // send post to these links
  // ref: https://discord.com/developers/docs/resources/webhook#execute-webhook
  private static final String dbBackupLink = System.getenv("dbBackupLink");
  private static final String logsLink = System.getenv("logsBackupLink");

  

  public static TrustManager[] trustAllCerts = new TrustManager[]{
    new X509TrustManager() {
      public java.security.cert.X509Certificate[] getAcceptedIssuers() {
        return null;
      }
      public void checkClientTrusted(
        java.security.cert.X509Certificate[] certs, String authType) {}
        

      public void checkServerTrusted(
        java.security.cert.X509Certificate[] certs, String authType) {}
      
      
    }
  };

  

  
  public static int sendReq(SendReqBuilder params) throws Exception{

    

    // create a cert that trusts everything and set as default
    try {
      SSLContext sc = SSLContext.getInstance("SSL");
      sc.init(null, trustAllCerts, new java.security.SecureRandom());
      HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
    } catch (Exception e) {
      System.out.println(e);
    }
    StringBuilder command = new StringBuilder();
    command.append("curl -X POST -F 'payload_json={\"content\": \""+params.content+"\"}' ");
    for (Integer i = 0; i< params.filePaths.size(); i++){
      command.append("-F \"file"+i.toString()+"=@"+ params.filePaths.get(i)+"\" ");
    }
      
    command.append(params.url);
    System.out.println("Sent backup to "+params.url );
    ProcessBuilder processBuilder = new ProcessBuilder();
    processBuilder.command("bash", "-c", command.toString());

    Process process = processBuilder.start();
    int exitCode = process.waitFor();
    return exitCode;
    
  }

  public static class SendReqBuilder{
    private String url;
    private LinkedList<String> filePaths = new LinkedList<>();
    private String content;
    
    public SendReqBuilder setFilePaths(LinkedList<String> fp){
      this.filePaths = fp;
      return this;
    }
    public SendReqBuilder setURL(String url){
      this.url = url;
      return this;
    }
    public SendReqBuilder setContent(String content){
      this.content = content;
      return this;
    }
    public int build() throws Exception{
      if ((url == null) || (filePaths == new LinkedList<String>()) || (content == null)){
        System.out.println(url + filePaths + content);
        throw new RuntimeException("Set url, fp and content properly!!");
      }
      return sendReq(this);
    }
  }

  
  
  public static void main(String[] args){
    try{

      Runnable r = new Runnable() {

        @Override
        public void run() {
          try{
            SendReqBuilder sbDB = new SendReqBuilder();
            int res1 = sbDB.setURL(dbBackupLink)
              .setContent(new Date().toString())
              .setFilePaths(new LinkedList<String>(Arrays.asList("other/serverSettings.db", "other/snipe2.db", "other/userSettings.db")))
              .build();
            SendReqBuilder sbLog = new SendReqBuilder();
            int res2 = sbLog.setURL(logsLink)
              .setContent(new Date().toString())
              .setFilePaths(new LinkedList<String>(Arrays.asList("logs/discord.log")))
              .build();
          } catch (Exception e){
            System.out.println(e);
          }
         }
    
        
      };
      

      // creates an thread pool of size 1
      ScheduledExecutorService executor = Executors.newScheduledThreadPool ( 1 );
      try {
        executor.scheduleAtFixedRate ( r , 0L , 1L , TimeUnit.HOURS ); // ( runnable , initialDelay , period , TimeUnit )
        Thread.sleep (Long.MAX_VALUE); 
      } catch ( InterruptedException ex ) {
        // pass
      } finally {
        System.out.println ( "Achievement unlocked: impossible!" );
        executor.shutdown();
      }

      
    } catch (Exception e){
      System.out.println(e);
    }
    
  }
}