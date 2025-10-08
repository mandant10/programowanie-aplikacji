namespace MinesweeperAPI.Models;

public class Reward
{
    public string Name { get; set; } = string.Empty;
    public string Texture { get; set; } = string.Empty;
    public string RequiredDifficulty { get; set; } = string.Empty; // "easy", "medium", "hard"
    public bool IsUnlocked { get; set; }
}
