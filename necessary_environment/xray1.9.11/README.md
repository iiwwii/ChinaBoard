1. 使用基础爬虫爬取并对爬虫爬取的链接进行漏洞扫描

   ```
   xray webscan --basic-crawler http://example.com --html-output example.html
   ```

2. 使用 HTTP 代理进行被动扫描

   ```
   xray webscan --listen 127.0.0.1:7777 --html-output example.html
   ```

3. 只扫描单个 url，不使用爬虫

   ```
   xray webscan --url http://example.com --html-output example.com.html
   ```

4. 手动指定本次运行的插件:默认情况下，将会启用所有内置插件，可以使用下列命令指定本次扫描启用的插件。

   ```
   xray webscan --plugins cmd-injection,sqldet --url http://example.com
   xray webscan --plugins cmd-injection,sqldet --listen 127.0.0.1:7777
   xray subdomain --target example.com --text-output example.com.txt
   ```

5. 指定输出格式:可以指定将本次扫描的漏洞信息输出到某个文件中，总共三种输出格式。

   ```
   xray webscan --url http://example.com --text-output result.txt --json-output result.json --html-output report.html
   ```

6. rad代理爬虫命令

   ```
   ./rad.exe -t http://example.com -http-proxy 127.0.0.1:7777
   ```

7. 用友NC NCMessageServlet反序列化漏洞。

   ```
   xray ws --poc poc-yaml-yongyou-nc-ncmessageservlet-rce --url http://example.com
   ```

   

