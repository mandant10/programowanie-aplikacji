namespace MinesweeperAPI.Models;

public class GameScore
{
    public int Id { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public string Difficulty { get; set; } = string.Empty; // "easy", "medium", "hard"
    public int TimeSeconds { get; set; }
    public DateTime PlayedAt { get; set; } = DateTime.UtcNow;
}
