FROM silviof/docker-languagetool:latest
# Expose 8010 by default in base image
CMD ["/bin/sh","-c","java -cp /LanguageTool/* org.languagetool.server.HTTPServer --port 8010 --public --allow-origin '*'"]
