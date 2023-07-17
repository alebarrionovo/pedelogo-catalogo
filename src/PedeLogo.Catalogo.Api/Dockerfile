FROM alebarrionovo/pedelogo-catalogo:v1.0.0
WORKDIR /app
EXPOSE 80
EXPOSE 443
WORKDIR /src
COPY . .
ENTRYPOINT ["dotnet", "PedeLogo.Catalogo.Api.dll"]
