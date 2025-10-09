# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app

# Copy published app
COPY --from=build /app/publish .

# Expose port
EXPOSE 5022

# Set environment
ENV ASPNETCORE_URLS=http://+:5022

# Run the app
ENTRYPOINT ["dotnet", "MinesweeperAPI.dll"]
