import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;

public class Player implements Serializable {
    /**
     * This class contains attributes of the player in the game.
     * */

    // Initialising private attributes of Player class
    private String name;
    private BigDecimal coins = new BigDecimal("1E6");
    private int coinsPerTurn = 0; // initial value
    private int level = 0; // initial value
    private BigDecimal exp = new BigDecimal("0");
    private BigDecimal expPerTurn = new BigDecimal("0"); // initial value
    private int totalMultiplier = 1; // initial value
    private BigDecimal requiredExp = new BigDecimal("5E5");
    private ArrayList<Place> ownedList = new ArrayList<>();
    private ArrayList<Upgrade> upgradeList = new ArrayList<>();
    private ArrayList<Card> cardList = new ArrayList<>();
    private int location = 0;

    // Creating constructor of Player class
    public Player(String name){
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public BigDecimal getCoins() {
        return coins;
    }

    public void setCoins(BigDecimal coins) {
        this.coins = coins;
    }

    public int getCoinsPerTurn() {
        return coinsPerTurn;
    }

    public void setCoinsPerTurn(int coinsPerTurn) {
        this.coinsPerTurn = coinsPerTurn;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public BigDecimal getExp() {
        return exp;
    }

    public void setExp(BigDecimal exp) {
        this.exp = exp;
    }

    public BigDecimal getExpPerTurn() {
        return expPerTurn;
    }

    public void setExpPerTurn(BigDecimal expPerTurn) {
        this.expPerTurn = expPerTurn;
    }

    public int getTotalMultiplier() {
        return totalMultiplier;
    }

    public void setTotalMultiplier(int totalMultiplier) {
        this.totalMultiplier = totalMultiplier;
    }

    public BigDecimal getRequiredExp() {
        return requiredExp;
    }

    public void setRequiredExp(BigDecimal requiredExp) {
        this.requiredExp = requiredExp;
    }

    public ArrayList<Place> getOwnedList() {
        return ownedList;
    }

    public void setOwnedList(ArrayList<Place> ownedList) {
        this.ownedList = ownedList;
    }

    public ArrayList<Upgrade> getUpgradeList() {
        return upgradeList;
    }

    public void setUpgradeList(ArrayList<Upgrade> upgradeList) {
        this.upgradeList = upgradeList;
    }

    public ArrayList<Card> getCardList() {
        return cardList;
    }

    public void setCardList(ArrayList<Card> cardList) {
        this.cardList = cardList;
    }

    public int getLocation() {
        return location;
    }

    public void setLocation(int location) {
        this.location = location;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this){
            return true;
        }

        if (!obj.getClass().equals(this.getClass())){
            return false;
        }

        if (obj instanceof Player){
            return name.equals(((Player) obj).name) && coins.equals(((Player) obj).coins) &&
                    coinsPerTurn == ((Player) obj).coinsPerTurn && level == ((Player) obj).level &&
                    exp.equals(((Player) obj).exp) && expPerTurn.equals(((Player) obj).expPerTurn) &&
                    totalMultiplier == ((Player) obj).totalMultiplier && requiredExp.equals(((Player) obj).requiredExp) &&
                    ownedList.equals(((Player) obj).ownedList) && upgradeList.equals(((Player) obj).upgradeList) &&
                    cardList.equals(((Player) obj).cardList) && location == ((Player) obj).location;
        }
        return false;
    }
}
