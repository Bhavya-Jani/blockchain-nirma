import { useState, useEffect } from "react";
import { ethers } from "ethers";
import { Connection, PublicKey } from "@solana/web3.js";
import { Provider, RpcProvider } from "starknet";

const WalletConnection = () => {
  const [walletAddress, setWalletAddress] = useState(null);
  const [walletBalance, setWalletBalance] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedWallet, setSelectedWallet] = useState("Select Wallet");
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    checkWalletConnection();
  }, []);

  const resetWallet = () => {
    setWalletAddress(null);
    setWalletBalance(null);
    setErrorMessage("");
  };

  const checkWalletConnection = async () => {
    if (window.ethereum) {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const accounts = await provider.send("eth_accounts", []);
        if (accounts.length > 0) {
          setWalletAddress(accounts[0]);
          setSelectedWallet("MetaMask ✅");
          fetchEthereumBalance(accounts[0]);
        }
      } catch (error) {
        console.error("Error checking MetaMask:", error);
      }
    }
  };

  const fetchEthereumBalance = async (address) => {
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const balance = await provider.getBalance(address);
      setWalletBalance(ethers.formatEther(balance));
    } catch (error) {
      setErrorMessage("Failed to fetch Ethereum balance.");
    }
  };

  const fetchSolanaBalance = async (address) => {
    try {
      const connection = new Connection("https://solana-mainnet.g.alchemy.com/v2/jTiRmRAcsAXUgxQXa3qO-HmoZFcSbKtj");
      const publicKey = new PublicKey(address);
      const balance = await connection.getBalance(publicKey);
      setWalletBalance((balance / 1e9).toFixed(6) + " SOL");
    } catch (error) {
      setErrorMessage("Failed to fetch Solana balance.");
    }
  };

  const fetchStarknetBalance = async (address) => {
    try {
      const provider = new RpcProvider({ nodeUrl: "https://alpha-mainnet.starknet.io" });
      const balance = await provider.getBalance(address);
      setWalletBalance(balance.toString() + " STRK");
    } catch (error) {
      setErrorMessage("Failed to fetch Starknet balance.");
    }
  };

  const connectMetaMask = async () => {
    resetWallet();
    if (window.ethereum) {
      try {
        await window.ethereum.request({ method: "eth_requestAccounts" });
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const address = await signer.getAddress();
        setWalletAddress(address);
        setSelectedWallet("MetaMask ✅");
        fetchEthereumBalance(address);
      } catch (error) {
        setErrorMessage("MetaMask connection failed.");
      }
    } else {
      setErrorMessage("MetaMask is not installed.");
    }
  };

  const connectSolanaWallet = async () => {
    resetWallet();
    if (window.solana && window.solana.isPhantom) {
      try {
        const response = await window.solana.connect();
        const address = response.publicKey.toString();
        setWalletAddress(address);
        setSelectedWallet("Phantom (Solana) ✅");
        fetchSolanaBalance(address);
      } catch (error) {
        setErrorMessage("Solana wallet connection failed.");
      }
    } else {
      setErrorMessage("Phantom Wallet is not installed.");
    }
  };

  const connectStarknetWallet = async () => {
    resetWallet();
    try {
      if (window.starknet && window.starknet.enable) {
        await window.starknet.enable();
        const accounts = window.starknet.selectedAddress || window.starknet.account?.address;
        if (accounts) {
          setWalletAddress(accounts);
          setSelectedWallet("Starknet ✅");
          fetchStarknetBalance(accounts);
        } else {
          setErrorMessage("No Starknet account found.");
        }
      } else {
        setErrorMessage("Starknet wallet not found. Make sure Argent X or another Starknet-compatible wallet is installed.");
      }
    } catch (error) {
      setErrorMessage("Starknet connection failed.");
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-4">
      <h2 className="text-2xl font-semibold mb-4">Blockchain Wallet Demo</h2>
      <div className="w-96 bg-white shadow-lg rounded-2xl p-6 mb-4">
        <h3 className="text-xl text-center mb-4">Connect Your Wallet</h3>
        <div className="relative">
          <button onClick={() => setDropdownOpen(!dropdownOpen)} className="w-full bg-blue-500 text-white px-4 py-2 rounded-md flex justify-between items-center hover:bg-blue-600 transition duration-200">
            {selectedWallet} ▼
          </button>
          {dropdownOpen && (
            <div className="absolute w-full mt-2 bg-white border rounded-md shadow-md z-10">
              <p className="p-3 cursor-pointer hover:bg-blue-100 transition duration-200" onClick={() => { setDropdownOpen(false); connectMetaMask(); }}>🦊 MetaMask</p>
              <p className="p-3 cursor-pointer hover:bg-green-100 transition duration-200" onClick={() => { setDropdownOpen(false); connectSolanaWallet(); }}>🔮 Phantom (Solana)</p>
            </div>
          )}
        </div>
        {walletAddress && <p className="text-green-600 text-center mt-2">✅ Connected: {walletAddress}</p>}
        {walletBalance !== null && <p className="text-blue-600 text-center mt-2">💰 Balance: {walletBalance}</p>}
        {errorMessage && <p className="text-red-500 text-center mt-2">⚠️ {errorMessage}</p>}
      </div>
    </div>
  );
};

export default WalletConnection;
