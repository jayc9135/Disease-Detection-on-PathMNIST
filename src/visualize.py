import matplotlib.pyplot as plt
import csv
import os

def load_metrics(num_rounds, attack):
    client_losses = {}
    client_accuracies = {}
    avg_losses = []
    avg_accuracies = []

    for r in range(1, num_rounds + 1):
        if attack:
            filename = f'results/metrics/attack/metrics_round_{r}.csv'
        else:
            filename = f'results/metrics/no_attack/metrics_round_{r}.csv'
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            continue

        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == 'Average':
                    avg_losses.append(float(row[1]))
                    avg_accuracies.append(float(row[2]))
                else:
                    cid = row[0]
                    loss = float(row[1])
                    accuracy = float(row[2])

                    if cid not in client_losses:
                        client_losses[cid] = []
                        client_accuracies[cid] = []
                    client_losses[cid].append(loss)
                    client_accuracies[cid].append(accuracy)

    return client_losses, client_accuracies, avg_losses, avg_accuracies

def plot_metrics(num_rounds, client_losses, client_accuracies, avg_losses, avg_accuracies, attack=False):
    rounds = list(range(1, num_rounds + 1))

    if attack:
        directory ='results/plots/attack'
    else:
        directory ='results/plots/no_attack'
    os.makedirs(directory, exist_ok=True)

    # 1. History of loss per client over rounds
    plt.figure(figsize=(10, 6))
    for cid, losses in client_losses.items():
        plt.plot(rounds[:len(losses)], losses, label=f"Client {cid}")
    plt.title("Loss per Client Over Rounds" + (" (With Attack)" if attack else " (Without Attack)"))
    plt.xlabel("Round")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{directory}/loss_per_client{'_attack' if attack else ''}.png")
    plt.show()

    # 2. History of average loss among clients over rounds
    plt.figure(figsize=(10, 6))
    plt.plot(rounds[:len(avg_losses)], avg_losses)
    # plt.plot(rounds[:len(avg_losses)], avg_losses, marker='o')
    plt.title("Average Loss Among Clients Over Rounds" + (" (With Attack)" if attack else " (Without Attack)"))
    plt.xlabel("Round")
    plt.ylabel("Average Loss")
    plt.grid(True)
    plt.savefig(f"{directory}/average_loss{'_attack' if attack else ''}.png")
    plt.show()

    # 3. History of evaluation accuracy per client over rounds
    plt.figure(figsize=(10, 6))
    for cid, accuracies in client_accuracies.items():
        plt.plot(rounds[:len(accuracies)], accuracies, label=f"Client {cid}")
    plt.title("Accuracy per Client Over Rounds" + (" (With Attack)" if attack else " (Without Attack)"))
    plt.xlabel("Round")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{directory}/accuracy_per_client{'_attack' if attack else ''}.png")
    plt.show()

    # 4. History of average evaluation accuracy among clients over rounds
    plt.figure(figsize=(10, 6))
    plt.plot(rounds[:len(avg_accuracies)], avg_accuracies)
    # plt.plot(rounds[:len(avg_accuracies)], avg_accuracies, marker='o')
    plt.title("Average Accuracy Among Clients Over Rounds" + (" (With Attack)" if attack else " (Without Attack)"))
    plt.xlabel("Round")
    plt.ylabel("Average Accuracy")
    plt.grid(True)
    plt.savefig(f"{directory}/average_accuracy{'_attack' if attack else ''}.png")
    plt.show()

if __name__ == "__main__":
    num_rounds = 100
    # Visualize without attack
    attack=False
    client_losses, client_accuracies, avg_losses, avg_accuracies = load_metrics(num_rounds, attack)
    plot_metrics(num_rounds, client_losses, client_accuracies, avg_losses, avg_accuracies, attack)


    # Visualize with attack
    attack=True
    client_losses, client_accuracies, avg_losses, avg_accuracies = load_metrics(num_rounds, attack)
    plot_metrics(num_rounds, client_losses, client_accuracies, avg_losses, avg_accuracies, attack)
