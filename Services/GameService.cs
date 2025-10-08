using System.Collections.Concurrent;
using MinesweeperAPI.Models;

namespace MinesweeperAPI.Services;

public interface IGameService
{
    Task<GameScore> SaveScoreAsync(GameScore score);
    Task<List<GameScore>> GetTopScoresAsync(string? difficulty = null, int limit = 10);
    Task<PlayerProgress> GetPlayerProgressAsync(string playerName);
    Task<PlayerProgress> UpdatePlayerProgressAsync(string playerName, string difficulty);
    Task<List<Reward>> GetRewardsAsync(string playerName);
}

public class GameService : IGameService
{
    private readonly ConcurrentBag<GameScore> _scores = new();
    private readonly ConcurrentDictionary<string, PlayerProgress> _progress = new();
    private int _scoreIdCounter = 1;
    private int _progressIdCounter = 1;

    public Task<GameScore> SaveScoreAsync(GameScore score)
    {
        score.Id = Interlocked.Increment(ref _scoreIdCounter);
        score.PlayedAt = DateTime.UtcNow;
        _scores.Add(score);
        return Task.FromResult(score);
    }

    public Task<List<GameScore>> GetTopScoresAsync(string? difficulty = null, int limit = 10)
    {
        var query = _scores.AsEnumerable();
        
        if (!string.IsNullOrEmpty(difficulty))
        {
            query = query.Where(s => s.Difficulty.Equals(difficulty, StringComparison.OrdinalIgnoreCase));
        }

        var topScores = query
            .OrderBy(s => s.TimeSeconds)
            .Take(limit)
            .ToList();

        return Task.FromResult(topScores);
    }

    public Task<PlayerProgress> GetPlayerProgressAsync(string playerName)
    {
        var progress = _progress.GetOrAdd(playerName, name => new PlayerProgress
        {
            Id = Interlocked.Increment(ref _progressIdCounter),
            PlayerName = name,
            CurrentTexture = "default"
        });

        return Task.FromResult(progress);
    }

    public Task<PlayerProgress> UpdatePlayerProgressAsync(string playerName, string difficulty)
    {
        var progress = _progress.GetOrAdd(playerName, name => new PlayerProgress
        {
            Id = Interlocked.Increment(ref _progressIdCounter),
            PlayerName = name,
            CurrentTexture = "default"
        });

        // Aktualizuj ukończone poziomy
        switch (difficulty.ToLower())
        {
            case "easy":
                progress.EasyCompleted = true;
                if (progress.CurrentTexture == "default")
                    progress.CurrentTexture = "bronze";
                break;
            case "medium":
                progress.MediumCompleted = true;
                if (progress.CurrentTexture == "default" || progress.CurrentTexture == "bronze")
                    progress.CurrentTexture = "silver";
                break;
            case "hard":
                progress.HardCompleted = true;
                progress.CurrentTexture = "gold";
                break;
        }

        return Task.FromResult(progress);
    }

    public Task<List<Reward>> GetRewardsAsync(string playerName)
    {
        var progress = _progress.GetOrAdd(playerName, name => new PlayerProgress
        {
            Id = Interlocked.Increment(ref _progressIdCounter),
            PlayerName = name,
            CurrentTexture = "default"
        });

        var rewards = new List<Reward>
        {
            new Reward
            {
                Name = "Brązowa tekstura",
                Texture = "bronze",
                RequiredDifficulty = "easy",
                IsUnlocked = progress.EasyCompleted
            },
            new Reward
            {
                Name = "Srebrna tekstura",
                Texture = "silver",
                RequiredDifficulty = "medium",
                IsUnlocked = progress.MediumCompleted
            },
            new Reward
            {
                Name = "Złota tekstura",
                Texture = "gold",
                RequiredDifficulty = "hard",
                IsUnlocked = progress.HardCompleted
            }
        };

        return Task.FromResult(rewards);
    }
}
