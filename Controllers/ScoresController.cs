using Microsoft.AspNetCore.Mvc;
using MinesweeperAPI.Models;
using MinesweeperAPI.Services;

namespace MinesweeperAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ScoresController : ControllerBase
{
    private readonly IGameService _gameService;

    public ScoresController(IGameService gameService)
    {
        _gameService = gameService;
    }

    /// <summary>
    /// Zapisz nowy wynik gry
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<GameScore>> PostScore([FromBody] GameScore score)
    {
        if (string.IsNullOrWhiteSpace(score.PlayerName) || score.PlayerName.Length > 50)
        {
            return BadRequest("PlayerName jest wymagane i nie może przekraczać 50 znaków");
        }

        if (!new[] { "easy", "medium", "hard" }.Contains(score.Difficulty.ToLower()))
        {
            return BadRequest("Difficulty musi być: easy, medium lub hard");
        }

        if (score.TimeSeconds <= 0)
        {
            return BadRequest("TimeSeconds musi być większe od 0");
        }

        var savedScore = await _gameService.SaveScoreAsync(score);
        
        // Aktualizuj postęp gracza
        await _gameService.UpdatePlayerProgressAsync(score.PlayerName, score.Difficulty);

        return CreatedAtAction(nameof(GetTopScores), new { difficulty = score.Difficulty }, savedScore);
    }

    /// <summary>
    /// Pobierz najlepsze wyniki
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<List<GameScore>>> GetTopScores(
        [FromQuery] string? difficulty = null,
        [FromQuery] int limit = 10)
    {
        if (limit < 1 || limit > 100)
        {
            return BadRequest("Limit musi być między 1 a 100");
        }

        var scores = await _gameService.GetTopScoresAsync(difficulty, limit);
        return Ok(scores);
    }
}
